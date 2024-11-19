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
  s3_bucket     = "pgr301-couch-explorers-kandidat42" # S3-bucket for lagring av bilder
  s3_key        = "lambda_sqs.zip" # Lambda-koden (zip-fil som inneholder koden)

  runtime = "python3.8"
  handler = "lambda_sqs.lambda_handler" # Funksjonen som kjører når Lambda trigges

  environment {
    variables = {
      SQS_QUEUE_URL = aws_sqs_queue.image_queue.url
    }
  }

  role = aws_iam_role.lambda_exec_role.arn
}

terraform {
  backend "s3" {
    bucket = "pgr301-2024-terraform-state-42"
    key    = "terraform.tfstate"
    region = "eu-west-1"
  }
}
