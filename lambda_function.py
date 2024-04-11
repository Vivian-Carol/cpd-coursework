import boto3
import json
import re

def lambda_handler(event, context):
    print("Event:", event)
    
    # Initialize Rekognition and DynamoDB clients
    rekognition_client = boto3.client('rekognition')
    dynamodb_client = boto3.client('dynamodb')
    
    try:
        # Attempt to extract the image file name directly from the body
        my_image = json.loads(event['Records'][0]['body'])['image_file_name']
    except KeyError:
        # If the direct extraction fails, try extracting from the nested structure
        try:
            nested_body = json.loads(event['Records'][0]['body'])
            my_image = nested_body['Records'][0]['s3']['object']['key']
        except KeyError:
            print("Image file name not found in the event.")
            return {
                'statusCode': 400,
                'body': json.dumps('Image file name not found in the event.')
            }
    
    print(f"Image file name: {my_image}")
    
    # Specify the S3 bucket name and the image file name
    bucket_name = 'mybucket-otuoma-caroline-s2110913'
    image_uri = f's3://{bucket_name}/{my_image}'
    
    print(f'Checking image_uri: {image_uri}')
    
    # Use Amazon Rekognition to detect labels in the image
    response = rekognition_client.detect_labels(
        Image={'S3Object': {'Bucket': bucket_name, 'Name': my_image}},
        MaxLabels=10,
        MinConfidence=80
    )
    vehicle_types = ['Car', 'Van', 'Truck']
    
    filtered_labels = [label for label in response['Labels'] if label['Name'] in vehicle_types]
    
    # Use Amazon Rekognition to detect text in the image
    response = rekognition_client.detect_text(Image={'S3Object': {'Bucket': bucket_name, 'Name': my_image}})
    
    # Updated regex to match typical number plate formats with either four or five digits
    number_plate_regex = re.compile(r'^\d{4,5} \w{2} \d{2}$')
    
    number_plate = ""
    number_plate_confidence = 0
    potential_number_plate = ""
    potential_number_plate_confidence = 0
    for text_detection in response['TextDetections']:
        if text_detection['Type'] == 'LINE':
            # Attempt to match the detected text with the number plate regex
            match = number_plate_regex.match(text_detection['DetectedText'])
            if match:
                number_plate += text_detection['DetectedText'] + " "
                number_plate_confidence += text_detection['Confidence']
            else:
                # Check if the line could be part of a number plate
                if re.match(r'\d{4,5}|\w{2}|\d{2}', text_detection['DetectedText']):
                    # Combine the line with the potential number plate
                    potential_number_plate += text_detection['DetectedText'] + " "
                    potential_number_plate_confidence += text_detection['Confidence']
                else:
                    # If the line doesn't match, check if the potential number plate matches the pattern
                    if number_plate_regex.match(potential_number_plate.strip()):
                        number_plate = potential_number_plate.strip()
                        
                        number_plate_confidence += potential_number_plate_confidence
                        
                        # Reset potential number plate for the next sequence
                        potential_number_plate = ""
                        potential_number_plate_confidence = 0
                    else:
                        # If the potential number plate doesn't match, reset it
                        potential_number_plate = ""
                        potential_number_plate_confidence = 0
    
    # Check the last potential number plate
    if number_plate_regex.match(potential_number_plate.strip()):
        number_plate = potential_number_plate.strip()
        
        number_plate_confidence += potential_number_plate_confidence
    
    # Calculating average confidence for number plate
    if response['TextDetections']:
        number_plate_confidence /= len(response['TextDetections'])
    
    # Storing data in DynamoDB
    for index, label in enumerate(filtered_labels):
        
        label_key = label['Name']
        
        dynamodb_client.put_item(
            TableName='Entry-Otuoma-Caroline-s2110913',
            Item={
                'ImageName': {'S': my_image},
                'Label': {'S': label_key},
                'LabelConfidence': {'N': str(label['Confidence'])},
                'NumberPlate': {'S': number_plate.strip()},
                'NumberPlateConfidence': {'N': str(number_plate_confidence)}
            }
        )
    
    return {
        'statusCode': 200,
        'body': json.dumps('Data extracted and stored successfully')
    }
