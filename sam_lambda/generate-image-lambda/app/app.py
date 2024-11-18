import base64
import boto3
import json
import os
import random

# Sett opp AWS-klienter for Bedrock og S
bedrock_client = boto3.client("bedrock-runtime", region_name="us-east-1")  # Bruk us-east-1 for Bedrock API
s3_client = boto3.client("s3", region_name="eu-west-1")  # Bruk eu-west-1 for S3 (Irland)

# Hent dynamisk bucket-navnet fra miljøvariabel
bucket_name = os.environ["S3_BUCKET_NAME"]

def lambda_handler(event, context):
    try:
        print("Received event: ", json.dumps(event))  # Logg hele eventet for feilsøking
        # Hent prompt fra HTTP POST body
        body = json.loads(event["body"])
        prompt = body["prompt"]
        print(f"Generating image for prompt: {prompt}")  # Logg prompten

        seed = random.randint(0, 2147483647)
        s3_image_path = f"generated_images/titan_{seed}.png"
        print(f"Generated image path: {s3_image_path}")

        # Bygg forespørselen for generering av bildet
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

        # Logg før vi kaller Bedrock API
        print("Calling Bedrock API to generate image...")
        response = bedrock_client.invoke_model(modelId="amazon.titan-image-generator-v1", body=json.dumps(native_request))
        print(f"Received response from Bedrock: {response}")  # Logg svaret fra Bedrock API

        model_response = json.loads(response["body"].read())
        print(f"Model response: {model_response}")  # Logg modellens svar

        # Ekstraher og dekod base64-bildedata
        base64_image_data = model_response["images"][0]
        image_data = base64.b64decode(base64_image_data)

        # Logg før vi laster opp bildet til S3
        print(f"Uploading image to S3 path: {s3_image_path}")
        s3_client.put_object(Bucket=bucket_name, Key=s3_image_path, Body=image_data)

        # Returner en suksessrespons
        return {
            "statusCode": 200,
            "body": json.dumps({"imageUrl": f"s3://{bucket_name}/{s3_image_path}"})
        }
    except Exception as e:
        print("Error occurred: ", str(e))  # Logg eventuelle feil
        return {
            "statusCode": 500,
            "body": json.dumps({"message": "Internal Server Error", "error": str(e)})
        }
