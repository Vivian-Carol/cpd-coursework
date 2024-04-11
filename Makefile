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

upload_images_to_ec2:
	@echo "Uploading to EC2 Instance..."
	@python upload_images_to_ec2.py

upload_images_to_s3:
	@echo "Uploading images form EC2 Instance to S3 Bucket..."
	@python upload_images_to_s3.py

# deploy: create_ec2_instance create_s3_bucket create_sqs_stack
# 	@echo "Deployment completed successfully."

deploy: upload_images_to_ec2 upload_images_to_s3
	@echo "Uploading Images to EC2  Instance..."