# AWS User Access Provision

This project automates the provisioning of AWS IAM users, groups, and policies, ensuring secure and scalable access management.

## File Structure

```
|---config
| └──settings.py # Application settings configuration
|---services
| └──services.py # Core logic for creating users, managing groups, and provisioning access.
|---utils
| └──logger.py # Logging events and errors
|---logs
| └──audit_log.json # Stores audit logs  
|---main.py # Orchestrates the AWS user provisioning process
|---requirements.txt
|---user_config.yaml # Configuration with user and group details
└── Readme.md # This file
```

## Prerequisites

1. **Python**
2. **AWS CLI**
3. **Python Libraries**

## Quick Start

1. **Clone or Download Configuration Files**

   - Obtain the project files from the repository.

2. **Set Up Virtual Environment and Install Dependencies**

   - Create and activate the virtual environment:
     - `python -m venv .venv`
     - Windows Command Prompt
     - `.venv\Scripts\activate.bat`
     - Windows PowerShell
     - `.venv\Scripts\Activate.ps1`
     - Mac/Linux Terminal
     - `source .venv/bin/activate`
   - Install dependencies:
     - `pip install -r requirements.txt`

3. **Configure AWS CLI**

   - Run `aws configure` in the terminal.
   - Provide `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, and `AWS_DEFAULT_REGION`.

4. **Update Configuration File**

   - Edit `user_config.yaml` to define user and group details.
   - Ensure all user permissions and details are accurate.

5. **Run the Application**

   - Execute the application:
     - `python main.py`

6. **Verify User Access Provisioning**

   - Check the following to confirm successful provisioning:
     - Logs in the `/logs` folder for application output.
     - Terminal summary of created users.
     - AWS account to verify user access.

7. **View Audit Logs**
   - The last run audit log can be found in the `/logs` folder as a JSON file.

## Example run and output

### Output

```
=== Summary ===
Successfully created 2 users
Failed to create 0 users
Created 2 groups

User: Srimathi
ARN: arn:aws:iam::*********:user/Srimathi
Console Access: True
Programmatic Access: True
Temporary Password: *************
Access Key ID: *********

User: Suresh
ARN: arn:aws:iam::*********:user/Suresh
Console Access: True
Programmatic Access: False
Temporary Password: ***********
```

### Screenshot

![AWS User Access Provising Sample Output screenshot](https://github.com/user-attachments/assets/360278fc-10c4-41b9-a61e-c30a3505372f)

## Cleanup

- Manually delete users from AWS if required.
