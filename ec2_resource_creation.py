import boto3

def check_instance_exists(ec2_client, instance_name):
    instances = ec2_client.describe_instances(Filters=[{'Name': 'tag:Name', 'Values': [instance_name]}])
    return bool(instances['Reservations'])

def create_ec2_instance(instance_name):
    ec2_client = boto3.client('ec2', region_name='us-east-1')

    if check_instance_exists(ec2_client, instance_name):
        print(f"Instance '{instance_name}' already exists.")
        return

    instance_params = {
        'ImageId': 'ami-051f8a213df8bc089',
        'InstanceType': 't2.micro',
        'KeyName': 'vockey',
        'MaxCount': 1,
        'MinCount': 1,
        'TagSpecifications': [{
            'ResourceType': 'instance',
            'Tags': [{'Key': 'Name', 'Value': instance_name}]
        }]
    }

    response = ec2_client.run_instances(**instance_params)

    print(f"Instance '{instance_name}' created successfully with instance ID: {response['Instances'][0]['InstanceId']}")

if __name__ == "__main__":
    instance_name = 'Otuoma-Caroline-s2110913'
    create_ec2_instance(instance_name)
