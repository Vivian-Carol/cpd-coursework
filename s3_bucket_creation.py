import boto3

def create_s3_bucket(bucket_name, region='us-east-1'):
    s3_client = boto3.client('s3', region_name=region)

    try:
        s3_client.head_bucket(Bucket=bucket_name)
        print(f"Bucket '{bucket_name}' already exists.")
        return False
    except s3_client.exceptions.ClientError as e:
        if e.response['Error']['Code'] == '404':
            try:
                s3_client.create_bucket(Bucket=bucket_name)
                print(f"Bucket '{bucket_name}' created successfully in region '{region}'.")
                return True
            except Exception as e:
                print(f"Error creating bucket '{bucket_name}': {str(e)}")
                return False
        else:
            print(f"Error checking bucket '{bucket_name}': {str(e)}")
            return False
        
if __name__ == "__main__":
    bucket_name= "mybucket-otuoma-caroline-s2110913"
    create_s3_bucket(bucket_name)