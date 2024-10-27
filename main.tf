provider "aws" {
  region = "us-east-1"  # You can choose your preferred region
}

# Fetch the default VPC for the security group
data "aws_vpc" "default" {
  default = true
}

# Create the cheapest EC2 instance (t3.nano) with Docker, Nginx, and Certbot
resource "aws_instance" "dash_app" {
  ami           = "ami-052b9fbb6949f883a" # Amazon Linux 2 AMI
  instance_type = "t3.nano"               # Cheapest instance type
  key_name      = "my-ec2-key"          # Ensure you have an EC2 key pair for SSH access

  # Installing Docker, Nginx, and Certbot
  user_data = <<-EOF
              #!/bin/bash
              sudo yum update -y
              
              # Install Docker
              sudo amazon-linux-extras install docker -y
              sudo service docker start
              sudo usermod -a -G docker ec2-user

              # Install Nginx
              sudo amazon-linux-extras install nginx1.12 -y
              sudo systemctl start nginx
              sudo systemctl enable nginx
              
              # Install Certbot for SSL (Let's Encrypt)
              sudo yum install -y certbot python2-certbot-nginx

              # Set up Docker Compose
              sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
              sudo chmod +x /usr/local/bin/docker-compose

              # Open firewall for HTTP/HTTPS
              sudo firewall-cmd --permanent --add-service=http
              sudo firewall-cmd --permanent --add-service=https
              sudo firewall-cmd --reload
              EOF

  tags = {
    Name = "DashAppInstance"
  }
}

# Create a security group allowing HTTP/HTTPS traffic in the default VPC
resource "aws_security_group" "allow_http_https" {
  name        = "allow_http_https"
  description = "Allow HTTP and HTTPS traffic"
  vpc_id      = data.aws_vpc.default.id  # Use the default VPC ID

  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "AllowHTTPandHTTPS"
  }
}

