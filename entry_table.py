import boto3
import json

def create_entry_table_stack(stack_name, template_file_path):
    cloudformation_client = boto3.client('cloudformation')

    # Load the CloudFormation template from the JSON file
    with open(template_file_path, 'r') as file:
        template_body = json.load(file)

    # Check if the stack already exists
    existing_stacks = cloudformation_client.list_stacks(StackStatusFilter=['CREATE_COMPLETE', 'UPDATE_COMPLETE'])
    for stack in existing_stacks['StackSummaries']:
        if stack['StackName'] == stack_name:
            print(f"Stack '{stack_name}' already exists. Skipping stack creation.")
            return

    response = cloudformation_client.create_stack(
        StackName=stack_name,
        TemplateBody=json.dumps(template_body),
        Capabilities=['CAPABILITY_NAMED_IAM']
    )

    print(f"Stack '{stack_name}' created with StackId: {response['StackId']}")

create_entry_table_stack("MyEntryTableStack-Otuoma-Caroline-s2110913", "./entry_table_template.json")
