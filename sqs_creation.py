import boto3

def create_sqs_stack(sqs_stack_name, template_body):
    cloudformation_client = boto3.client('cloudformation')

    # Check if the stack already exists
    existing_stacks = cloudformation_client.list_stacks(StackStatusFilter=['CREATE_COMPLETE', 'UPDATE_COMPLETE'])
    for stack in existing_stacks['StackSummaries']:
        if stack['StackName'] == sqs_stack_name:
            print(f"Stack '{sqs_stack_name}' already exists. Skipping stack creation.")
            return

    try:
        response = cloudformation_client.create_stack(
            StackName=sqs_stack_name,
            TemplateBody=template_body,
            Capabilities=['CAPABILITY_NAMED_IAM']
        )
        print(f"Stack '{sqs_stack_name}' creation initiated.")
        print("Waiting for stack creation to complete...")
        waiter = cloudformation_client.get_waiter('stack_create_complete')
        waiter.wait(StackName=sqs_stack_name)
        print(f"Stack '{sqs_stack_name}' created successfully.")
    except Exception as e:
        print(f"Error creating stack '{sqs_stack_name}': {str(e)}")

if __name__ == "__main__":
    sqs_stack_name = 'MySQSStackOtuomaCarolineS2110913'
    with open('sqs_template.json', 'r') as template_file:
        template_body = template_file.read()

    create_sqs_stack(sqs_stack_name, template_body)
