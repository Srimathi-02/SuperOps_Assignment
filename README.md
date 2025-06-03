# Assignment 1: GCP Load Balancer Infrastructure

This project uses Terraform to create a complete load-balanced web application infrastructure on Google Cloud Platform (GCP).

## Key Features

- **VPC Network**: Custom subnet with Cloud NAT for outbound internet access.
- **Compute Instances**: Two web server instances running Nginx.
- **Global HTTP Load Balancer**: Configured with health checks and firewall rules.
- **Security**: Instance Access Protocol (IAP) for SSH access and restricted firewall rules.

# Assignment 2: AWS user access provision using Python

This project automates the provisioning of AWS IAM users, groups, and policies, ensuring secure and scalable access management.

## Key Features

- **Automated IAM User and Group Management**: Automatically creates AWS IAM users, assigns them to groups, and applies appropriate policies.
- **Configuration-Driven**: Uses a YAML configuration file (user_config.yaml) to define users, groups, and their respective permissions.
- **Audit Logging**: Logs all provisioning activities, including user creation and group assignments, to a log file (aws_user_provisioning.log) and audit logs in JSON format.
- **Secure Access**: Supports multi-factor authentication (MFA), programmatic access, and console access configurations for users.
- **Policy Management**: Attaches predefined AWS-managed policies to groups for fine-grained access control.

