.PHONY: create_ec2_instance

create_ec2_instance:
	@echo "Creating EC2 Instance in AWS Console..."
	@python ec2_resource_creation.py

create_s3_bucket:
	@echo "Creating S3 Bucket..."
	@python s3_bucket_creation.py

create_sqs_stack:
	@echo "Initialize SQS creation..."
	@python sqs_creation.py

create_entry_table_stack:
	@echo "Creating the DynamoDB Entry Table..."
	@python entry_table.py

create_vehicle_table_stack:
	@echo "Creating the DynamoDB Vehicle Table..."
	@python vehicle_table.py

populate_vehicle_table:
	@echo "Populating the table with Dummy Number Plates to check against..."
	@python populate_vehicle_table.py

upload_images_to_ec2:
	@echo "Uploading to EC2 Instance..."
	@python upload_images_to_ec2.py

upload_images_to_s3:
	@echo "Uploading images form EC2 Instance to S3 Bucket..."
	@python upload_images_to_s3.py

create_lambda_function:
	@echo "Initializing the First Lambda Function..."
	@python create_lambda_function.py

create_second_lambda_function:
	@echo "Initializing the Second Lambda Function..."
	@python second_lambda_function_creation.py

First_deploy: create_ec2_instance create_s3_bucket create_sqs_stack create_entry_table_stack create_vehicle_table_stack populate_vehicle_table
	@echo "Resource Creation completed successfully."

Second_deploy: upload_images_to_ec2 upload_images_to_s3 create_lambda_function create_second_lambda_function
	@echo "Operation successfully!!"