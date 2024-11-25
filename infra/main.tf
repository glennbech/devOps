terraform {
  required_version = ">= 1.9"
}

provider "aws" {
  region = "eu-west-1"
  version = "~> 5.74.0"
}

resource "aws_sqs_queue" "image_queue" {
  name = "image-processing-queue"
}

resource "aws_iam_role" "lambda_exec_role" {
  name = "lambda_execution_role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "lambda.amazonaws.com"
        }
      }
    ]
  })
}

resource "aws_lambda_function" "image_processor" {
  function_name = "imageProcessor"
  s3_bucket     = "pgr301-couch-explorers-kandidat42"
  s3_key        = "lambda_sqs.zip"

  runtime = "python3.8"
  handler = "lambda_sqs.lambda_handler"

  environment {
    variables = {
      SQS_QUEUE_URL = aws_sqs_queue.image_queue.url
      BUCKET_NAME = "pgr301-couch-explorers-kandidat42"
    }
  }

  role = aws_iam_role.lambda_exec_role.arn

  memory_size = 128
  timeout      = 30
}

# oppgave 4
resource "aws_cloudwatch_metric_alarm" "sqs_age_alarm" {
  alarm_name          = "SQS-ApproximateAgeOfOldestMessage-Alarm"
  comparison_operator = "GreaterThanThreshold"
  evaluation_periods  = 1
  metric_name         = "ApproximateAgeOfOldestMessage"
  namespace           = "AWS/SQS"
  period              = 60
  statistic           = "Maximum"
  threshold           = 80
  alarm_description   = "Triggered when the age of the oldest message in the queue exceeds threshold."

  dimensions = {
    QueueName = aws_sqs_queue.image_queue.name
  }

  alarm_actions = [aws_sns_topic.sqs_alarm_topic.arn]
}

resource "aws_sns_topic" "sqs_alarm_topic" {
  name = "sqs-alarm-topic"
}

resource "aws_sns_topic_subscription" "sqs_alarm_email" {
  endpoint = var.notification_email
  protocol = "email"
  topic_arn = aws_sns_topic.sqs_alarm_topic.arn
}

terraform {
  backend "s3" {
    bucket = "pgr301-2024-terraform-state-42"
    key    = "terraform.tfstate"
    region = "eu-west-1"
  }
}
