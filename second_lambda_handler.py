import boto3
import json

# Initialize the DynamoDB and SNS clients
dynamodb_client = boto3.client('dynamodb')
sns_client = boto3.client('sns')

def publish_to_sns(subject, message, topic_arn):
    print('we are here')
    try:
        response = sns_client.publish(
            TopicArn=topic_arn,
            Message=message,
            Subject=subject
        )
        print(f"SNS publish response: {response}")
        print("Alert sent successfully")
    except Exception as e:
        print(f"Error publishing to SNS: {e}")
        raise

def lambda_handler(event, context):
    print(f'event: {event}')
    for record in event['Records']:
        # Process only INSERT events
        if record['eventName'] == 'INSERT':
            new_image = record['dynamodb']['NewImage']
            number_plate = new_image['NumberPlate']['S']
            
            print(f'number_plate: {number_plate}')
            
            # Query the Vehicle table to check if the number plate is blacklisted
            response = dynamodb_client.query(
                TableName='VehicleTable-Otuoma-Caroline-s2110913',
                KeyConditionExpression='VehicleId = :VehicleId',
                ExpressionAttributeValues={
                    ':VehicleId': {'S': number_plate}
                }
            )
            
            if response['Count'] > 0:
                vehicle = response['Items'][0]
                
                print(f'vehicle: {vehicle}')
                
                if vehicle['status']['S'] == 'Blacklisted':
                    print('passed')
                    # Publish a message to the SNS topic
                    subject = 'Blacklisted Vehicle Detected'
                    message = f"A vehicle with the number plate {number_plate} has been detected and is blacklisted."
                    topic_arn = 'arn:aws:sns:us-east-1:105310011039:BlacklistedVehicleNotifications'
                    publish_to_sns(subject, message, topic_arn)
                    

    return {
        'statusCode': 200,
        'body': json.dumps('Processed DynamoDB stream event.')
    }
