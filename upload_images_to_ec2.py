import os

def upload_images_to_ec2(local_image_directory, instance_ip, pem_key):
    os.system(f'scp -i {pem_key} -r {local_image_directory} ec2-user@{instance_ip}:~/')

if __name__ == "__main__":
    local_image_directory = "./Images/"
    instance_ip = "3.83.116.36"
    pem_key = "vockey.pem"

    upload_images_to_ec2(local_image_directory, instance_ip, pem_key)