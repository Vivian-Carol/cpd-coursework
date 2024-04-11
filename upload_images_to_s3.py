import boto3
import os
import time
import json

def upload_images_to_s3(bucket_name, local_image_directory, sqs_queue_url):
    s3_client = boto3.client('s3')
    sqs_client = boto3.client('sqs')
    image_files = os.listdir(local_image_directory)

    for image_file in image_files:

        if image_file.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.bmp')):
            s3_object_key = f"{image_file}"
            s3_client.upload_file(f"{local_image_directory}/{image_file}", bucket_name, s3_object_key)
            print(f"Image '{image_file}' uploaded to S3 bucket '{bucket_name}'.")
            
            # Send a message to SQS queue for each uploaded image file
            message_body = {
                'image_file_name': image_file
            }
            sqs_client.send_message(QueueUrl=sqs_queue_url, MessageBody=json.dumps(message_body))
            
            time.sleep(30)
        else:
            print(f"Skipping non-image file: {image_file}")

if __name__ == "__main__":
    bucket_name = 'mybucket-otuoma-caroline-s2110913'
    local_image_directory = './Images/'
    sqs_queue_url = 'https://sqs.us-east-1.amazonaws.com/105310011039/MySQS-Otuoma-Caroline-s2110913'
    upload_images_to_s3(bucket_name, local_image_directory, sqs_queue_url)
