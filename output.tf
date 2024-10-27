# Output public IP and SSH command for convenience
output "public_ip" {
  value       = aws_instance.dash_app.public_ip
  description = "Public IP of the EC2 instance"
}

# Output HTTPS URL for accessing the Dash app
output "dash_app_url_https" {
  value       = "https://${aws_instance.dash_app.public_ip}"
  description = "HTTPS URL to access the Dash app"
}

# Output SSH command to log in to the EC2 instance
output "ssh_command" {
  value       = "ssh -i ~/.ssh/your-ec2-key.pem ec2-user@${aws_instance.dash_app.public_ip}"
  description = "SSH command to connect to the EC2 instance"
}
