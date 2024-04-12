import boto3

def create_vehicle_table_stack(vehicle_table_stack_name, template_body):
    cloudformation_client = boto3.client('cloudformation')

    # Check if the stack already exists
    existing_stacks = cloudformation_client.list_stacks(StackStatusFilter=['CREATE_COMPLETE', 'UPDATE_COMPLETE'])
    for stack in existing_stacks['StackSummaries']:
        if stack['StackName'] == vehicle_table_stack_name:
            print(f"Stack '{vehicle_table_stack_name}' already exists. Skipping stack creation.")
            return

    response = cloudformation_client.create_stack(
        StackName=vehicle_table_stack_name,
        TemplateBody=template_body,
        Capabilities=['CAPABILITY_NAMED_IAM']
    )

    print(f"VehicleTable stack created with StackId: {response['StackId']}")

if __name__ == "__main__":
    vehicle_table_stack_name = 'VehicleTableStack-Otuoma-Caroline-s2110913'
    with open('vehicle_table.json', 'r') as file:
        template_body = file.read()
    create_vehicle_table_stack(vehicle_table_stack_name, template_body)
