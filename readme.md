# Project Overview

This project is a Dash application that allows users to explore the relationship between different salts (drugs) and their associated side effects using a 3D interactive network graph. The application is built with Python, Dash, and Plotly, and is deployed on AWS using Terraform for infrastructure management.

# Features
- Visualize salt compositions and their side effects in an interactive 3D network graph.
- Select multiple salts from a dropdown menu to view their side effects.
- Salts are represented in blue, and side effects are represented in green for easy differentiation.
- User-friendly interface with clear instructions and interactive capabilities.

# Technologies Used
- **Python**: The primary programming language for building the application.
- **Dash and Plotly**: Used for creating the interactive web interface and 3D visualizations.
- **NetworkX**: For creating the network graph structure.
- **Docker**: Containerization of the application for easy deployment.
- **AWS (EC2, S3)**: Hosting and infrastructure management.
- **Terraform**: Infrastructure as Code (IaC) for deploying and managing AWS resources.

# Installation and Setup

## Prerequisites
- Docker installed on your machine.
- AWS CLI configured for deploying the application to AWS.
- An EC2 key pair for SSH access.

## Clone the Repository
```
git clone <repository-url>
cd <repository-folder>
```

## Build and Run with Docker

1. Build the Docker image:
   ```
   docker build -t salt-side-effects-app .
   ```
2. Run the Docker container:
   ```
   docker run -p 8050:8050 salt-side-effects-app
   ```

The application will be accessible at `http://localhost:8050`.

# Usage
1. Navigate to the application URL 
   ```https://www.saltprojectabdulrahman.com
   ```
2. Select one or more salts from the dropdown menu.
3. Click the 'Submit' button to visualize the graph showing the selected salts and their side effects.
4. Interact with the graph by zooming, rotating, and exploring the connections.

# Deployment

## Using Terraform
The project includes Terraform configuration to deploy the application to AWS.

1. Initialize Terraform:
   ```
   terraform init
   ```
2. Apply the configuration:
   ```
   terraform apply
   ```

This will set up an EC2 instance running the application, along with a security group allowing HTTP/HTTPS access.

# Output Information
- Public IP of the EC2 instance.
- SSH command to connect to the instance.
- HTTPS URL to access the deployed Dash application.

Replace the `ami`, `key_name`, and any other variables in `main.tf` with your own AWS settings.

# Contributing
Feel free to fork the repository and submit pull requests. Any contributions are welcome!

# Contact
For any questions or suggestions, please reach out via [email address placeholder].

# License
This project is licensed under the MIT License.

