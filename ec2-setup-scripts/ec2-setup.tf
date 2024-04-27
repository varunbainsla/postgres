//Source : https://dev.to/johndotowl/postgresql-16-installation-on-ubuntu-2204-51ia

provider "aws" {
  region = "ap-south-1"
  profile = "dev"

  # Add your AWS credentials or configure them through other means
}

resource "aws_instance" "varun-ec2-same-az" {
  ami           = "ami-007020fd9c84e18c7" // Replace with your desired AMI ID
  instance_type = "t2.micro"
  key_name      = "test-ec2-1"     // Replace with your key pair name
#  security_groups = ["launch-wizard-48"] // Replace with your security group name
  subnet_id = "subnet-67d2640e" // AZ : ap-south-1a {Subnet Id for specifying Availability Zone }

  user_data = "${file("test.sh")}"

  tags = {
    Name = "varun-ec2-same-az"
  }
}

output "public_ip_same_az" {
  value = aws_instance.varun-ec2-same-az.public_ip
}

resource "aws_instance" "varun-ec2-different-az" {
  ami           = "ami-007020fd9c84e18c7" // Replace with your desired AMI ID
  instance_type = "t2.micro"
  key_name      = "test-ec2-1"     // Replace with your key pair name
#  security_groups = ["launch-wizard-48"] // Replace with your security group name
  subnet_id = "subnet-c1a2558c" // AZ :ap-south-1b  {Subnet Id for specifying Availability Zone }

  user_data = "${file("test.sh")}"

  tags = {
    Name = "varun-ec2-different-az"
  }
}

output "public_ip" {
  value = aws_instance.varun-ec2-different-az.public_ip
}