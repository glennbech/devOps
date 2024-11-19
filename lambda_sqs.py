import base64
import boto3
import json
import random
import os
import time
from botocore.exceptions import BotoCoreError

bedrock_client = boto3.client("bedrock-runtime", region_name="us-east-1")
s3_client = boto3.client("s3")

MODEL_ID = "amazon.titan-image-generator-v1"
BUCKET_NAME = os.environ["BUCKET_NAME"]

def lambda_handler(event, context):
    # Loop through all SQS records in the event
    for record in event["Records"]:
        prompt = record["body"]
        seed = random.randint(0, 2147483647)
        s3_image_path = f"images/titan_{seed}.png"

        native_request = {
            "taskType": "TEXT_IMAGE",
            "textToImageParams": {"text": prompt},
            "imageGenerationConfig": {
                "numberOfImages": 1,
                "quality": "standard",
                "cfgScale": 8.0,
                "height": 512,
                "width": 512,
                "seed": seed,
            },
        }

        # Retry logic with exponential backoff
        retries = 0
        max_retries = 5
        sleep_time = 1  # Initial sleep time in seconds

        while retries < max_retries:
            try:
                # Attempt to invoke the model
                response = bedrock_client.invoke_model(
                    modelId=MODEL_ID,
                    body=json.dumps(native_request)
                )

                model_response = json.loads(response["body"].read())
                base64_image_data = model_response["images"][0]
                image_data = base64.b64decode(base64_image_data)

                # Upload the image to S3
                s3_client.put_object(Bucket=BUCKET_NAME, Key=s3_image_path, Body=image_data)
                break  # If successful, exit retry loop

            except BotoCoreError as e:
                # Handle other boto3 exceptions
                if isinstance(e, BotoCoreError) and "Throttling" in str(e):
                    retries += 1
                    print(f"Throttling error occurred, retrying in {sleep_time} seconds...")
                    time.sleep(sleep_time)
                    sleep_time *= 2  # Exponential backoff: wait double the time for each retry
                else:
                    print(f"An error occurred: {e}")
                    break  # Exit the loop if other errors occur

        # If all retries fail, return a failure response
        if retries == max_retries:
            return {
                "statusCode": 500,
                "body": json.dumps("Max retries exceeded or another error occurred")
            }

    return {
        "statusCode": 200,
        "body": json.dumps("Images processed and uploaded successfully")
    }
