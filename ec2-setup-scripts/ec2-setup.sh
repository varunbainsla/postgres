#!/bin/bash
# EC2 Bash scrpit setup
# Define variables
INSTANCE_TYPE="t2.micro"
KEY_NAME="test-ec2-1"
SECURITY_GROUP_ID="sg-09cbf0afe85d1c65f"
AMI_ID="ami-007020fd9c84e18c7"
#USER_DATA_SCRIPT="user_data_script.sh"  # Path to your user data script

# Create EC2 instance
instance_id=$(aws ec2 run-instances \
    --image-id $AMI_ID \
    --instance-type $INSTANCE_TYPE \
    --key-name $KEY_NAME \
    --security-group-ids $SECURITY_GROUP_ID \
    --region "ap-south-1"\
    --query "Instances[0].InstanceId" \
    --tag-specifications 'ResourceType=instance,Tags=[{Key=Name,Value=varun-ec2}]' \
    --output text --profile dev)

echo "EC2 instance created with ID: $instance_id"

# Wait for instance to be in running state
aws ec2 wait instance-running --instance-ids $instance_id

# Get public IP address of the instance
public_ip=$(aws ec2 describe-instances \
    --instance-ids $instance_id \
    --query "Reservations[0].Instances[0].PublicIpAddress" \
    --output text --profile dev)

echo "Public IP address of the instance: $public_ip"

# Example: SSH into the instance and run commands
#ssh -i /path/to/your/keypair.pem ec2-user@$public_ip << EOF
#    # Run your commands here
#    echo "Hello from the EC2 instance!"
#    sudo yum update -y
#    # Add more commands as needed
#EOF
