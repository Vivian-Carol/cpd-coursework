import boto3
import zipfile

def create_lambda_function(lambda_function_name, sqs_queue_url):
    lambda_client = boto3.client('lambda')

    # Check if Lambda function already exists
    try:
        lambda_client.get_function(FunctionName=lambda_function_name)
        print("Lambda function already exists.")
    except lambda_client.exceptions.ResourceNotFoundException:
        # Create a ZIP archive of the Python file
        with zipfile.ZipFile('lambda_function.zip', 'w') as zipf:
            zipf.write('lambda_function.py')
        
        # Read the ZIP file
        with open('lambda_function.zip', 'rb') as f:
            code = f.read()

        # Create the Lambda function
        response = lambda_client.create_function(
            FunctionName=lambda_function_name,
            Runtime='python3.8',
            Role='arn:aws:iam::105310011039:role/LabRole',
            Handler='lambda_function.lambda_handler',
            Code={
                'ZipFile': code
            }
        )
        print("Lambda function created successfully.")

    # Check if event source mapping already exists
    mappings = lambda_client.list_event_source_mappings(FunctionName=lambda_function_name)
    if not mappings['EventSourceMappings']:
        # Configure the Lambda function to trigger from the SQS queue
        lambda_client.create_event_source_mapping(
            EventSourceArn=sqs_queue_url,
            FunctionName=lambda_function_name,
            Enabled=True
        )
        print("Event source mapping created successfully.")
    else:
        print("Event source mapping already exists.")

    print("Lambda function creation and configuration completed.")

if __name__ == "__main__":
    lambda_function_name = 'MyLambdaFunction-Otuoma-Caroline-s2110913'
    sqs_queue_url = 'arn:aws:sqs:us-east-1:105310011039:MySQS-Otuoma-Caroline-s2110913'

    create_lambda_function(lambda_function_name, sqs_queue_url)
