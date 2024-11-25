import base64
import boto3
import json
import os
import random

bedrock_client = boto3.client("bedrock-runtime", region_name="us-east-1")
s3_client = boto3.client("s3", region_name="eu-west-1")

bucket_name = os.environ["S3_BUCKET_NAME"]

def lambda_handler(event, context):
    try:
        print("Received event: ", json.dumps(event))
        body = json.loads(event["body"])
        prompt = body["prompt"]
        print(f"Generating image for prompt: {prompt}")

        seed = random.randint(0, 2147483647)
        s3_image_path = f"generated_images/titan_{seed}.png"
        print(f"Generated image path: {s3_image_path}")

        native_request = {
            "taskType": "TEXT_IMAGE",
            "textToImageParams": {"text": prompt},
            "imageGenerationConfig": {
                "numberOfImages": 1,
                "quality": "standard",
                "cfgScale": 8.0,
                "height": 1024,
                "width": 1024,
                "seed": seed,
            }
        }

        print("Calling Bedrock API to generate image...")
        response = bedrock_client.invoke_model(modelId="amazon.titan-image-generator-v1", body=json.dumps(native_request))
        print(f"Received response from Bedrock: {response}")

        model_response = json.loads(response["body"].read())
        print(f"Model response: {model_response}")

        base64_image_data = model_response["images"][0]
        image_data = base64.b64decode(base64_image_data)

        print(f"Uploading image to S3 path: {s3_image_path}")
        s3_client.put_object(Bucket=bucket_name, Key=s3_image_path, Body=image_data)

        return {
            "statusCode": 200,
            "body": json.dumps({"imageUrl": f"s3://{bucket_name}/{s3_image_path}"})
        }
    except Exception as e:
        print("Error occurred: ", str(e))
        return {
            "statusCode": 500,
            "body": json.dumps({"message": "Internal Server Error", "error": str(e)})
        }
