import boto3
import zipfile
import time

def create_second_lambda_function(lambda_function_name, dynamodb_table_name):
    lambda_client = boto3.client('lambda')
    dynamodb_client = boto3.client('dynamodb')

    # Check if Lambda function already exists
    try:
        lambda_client.get_function(FunctionName=lambda_function_name)
        print("Lambda function already exists.")
    except lambda_client.exceptions.ResourceNotFoundException:
        # Create a ZIP archive of the Python file
        with zipfile.ZipFile('second_lambda_function.zip', 'w') as zipf:
            zipf.write('second_lambda_handler.py')
        
        # Read the ZIP file
        with open('second_lambda_function.zip', 'rb') as f:
            code = f.read()

        # Create the Lambda function
        response = lambda_client.create_function(
            FunctionName=lambda_function_name,
            Runtime='python3.8',
            Role='arn:aws:iam::105310011039:role/LabRole',
            Handler='second_lambda_handler.lambda_handler',
            Code={
                'ZipFile': code
            }
        )
        print("Lambda function created successfully.")

    # Check if the stream is already enabled
    table_description = dynamodb_client.describe_table(TableName=dynamodb_table_name)
    if 'StreamSpecification' in table_description['Table'] and 'StreamEnabled' in table_description['Table']['StreamSpecification'] and table_description['Table']['StreamSpecification']['StreamEnabled']:
        print("Stream is already enabled on the DynamoDB table.")
        dynamodb_stream_arn = table_description['Table']['LatestStreamArn']
    else:
        # Enable a stream on the DynamoDB table if it's not already enabled
        try:
            dynamodb_client.update_table(
                TableName=dynamodb_table_name,
                StreamSpecification={
                    'StreamEnabled': True,
                    'StreamViewType': 'NEW_AND_OLD_IMAGES' # or 'KEYS_ONLY' or 'NEW_IMAGE'
                }
            )
            print("Stream enabled on the DynamoDB table.")
            # Wait for 10 seconds to give the stream a chance to activate
            print("Waiting for 10 seconds to give the DynamoDB stream a chance to activate...")
            time.sleep(10)
            # Extract the stream ARN after enabling the stream
            table_description = dynamodb_client.describe_table(TableName=dynamodb_table_name)
            dynamodb_stream_arn = table_description['Table']['LatestStreamArn']
        except dynamodb_client.exceptions.ResourceInUseException:
            print("Stream is already enabled on the DynamoDB table.")
            # Extract the stream ARN if the stream was already enabled
            dynamodb_stream_arn = table_description['Table']['LatestStreamArn']

    # Configure the Lambda function to trigger from the DynamoDB table with specific settings
    lambda_client.create_event_source_mapping(
        EventSourceArn=dynamodb_stream_arn,
        FunctionName=lambda_function_name,
        Enabled=True,
        BatchSize=100,
        StartingPosition='LATEST'
    )
    print("Event source mapping created successfully.")

if __name__ == "__main__":
    lambda_function_name = 'MySecondLambdaFunction-Otuoma-Caroline-s2110913'
    dynamodb_table_name = 'Entry-Otuoma-Caroline-s2110913'
    create_second_lambda_function(lambda_function_name, dynamodb_table_name)
