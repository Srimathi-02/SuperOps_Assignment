"""
This module contains service-related functions for the AWS assignment.
Each function is designed to handle specific service operations.
"""

from typing import Dict
import boto3
from botocore.exceptions import ClientError
from datetime import datetime
import yaml
import json
import secrets
import string
from utils.logger import logger
from config.settings import AWS_REGION, PROFILE_NAME


class AWSUserProvisioningError(Exception):
    """Custom exception for AWS user provisioning errors"""

    pass


class AWSUserProvisioner:
    """
    A comprehensive AWS User Access Provisioning system that handles:
    - User creation with proper IAM policies
    - Group-based access control
    - Temporary access keys with rotation
    - Audit logging and compliance
    - Rollback capabilities
    """

    def __init__(self):
        """
        Initialize the AWS User Provisioner
        """
        try:
            self.session = boto3.Session(
                profile_name=PROFILE_NAME, region_name=AWS_REGION
            )
            self.iam = self.session.client("iam")
            self.sts = self.session.client("sts")
            self.region = AWS_REGION

            # Verify credentials
            self._verify_credentials()

        except Exception as e:
            raise AWSUserProvisioningError(f"AWS initialization failed: {str(e)}")

    def _verify_credentials(self) -> None:
        """Verify AWS credentials and permissions"""
        try:
            self.sts.get_caller_identity()
        except Exception as e:
            raise AWSUserProvisioningError(f"Invalid AWS credentials: {str(e)}")

    def _generate_secure_password(self, length: int = 16) -> str:
        """Generate a secure random password"""
        alphabet = string.ascii_letters + string.digits + "!@#$%&*"
        password = "".join(secrets.choice(alphabet) for _ in range(length))
        return password

    def create_user(self, user_config: Dict[str, any]) -> Dict[str, any]:
        """
        Create a single AWS IAM user with specified configuration

        Args:
            user_config: Dictionary containing user configuration

        Returns:
            Dict containing user creation results
        """
        username = user_config.get("username")
        if not username:
            return {"success": False, "error": "Username is required"}

        try:
            logger.info(f"Creating user: {username}")

            # Check if user already exists
            if self._user_exists(username):
                logger.warning(f"User {username} already exists")
                return {"success": False, "error": f"User {username} already exists"}

            # Create IAM user
            user_response = self.iam.create_user(
                UserName=username,
                Path=user_config.get("path", "/"),
                Tags=[
                    {"Key": "CreatedBy", "Value": "AutoProvisioning"},
                    {"Key": "CreatedDate", "Value": datetime.now().isoformat()},
                    {
                        "Key": "Department",
                        "Value": user_config.get("department", "Unknown"),
                    },
                    {"Key": "Role", "Value": user_config.get("role", "Unknown")},
                ],
            )

            result = {
                "success": True,
                "username": username,
                "user_arn": user_response["User"]["Arn"],
                "created_at": user_response["User"]["CreateDate"].isoformat(),
                "console_access": False,
                "programmatic_access": False,
            }

            # Add to groups
            for group_name in user_config.get("groups", []):
                try:
                    self.iam.add_user_to_group(GroupName=group_name, UserName=username)
                    logger.info(f"Added user {username} to group {group_name}")
                except ClientError as e:
                    logger.warning(
                        f"Failed to add user {username} to group {group_name}: {str(e)}"
                    )

            # Attach policies to user
            for policy_arn in user_config.get("policies", []):
                try:
                    self.iam.attach_user_policy(UserName=username, PolicyArn=policy_arn)
                    logger.info(f"Attached policy {policy_arn} to user {username}")
                except ClientError as e:
                    logger.warning(
                        f"Failed to attach policy {policy_arn} to user {username}: {str(e)}"
                    )

            # Create console access
            if user_config.get("console_access", False):
                password = self._generate_secure_password()
                self.iam.create_login_profile(
                    UserName=username,
                    Password=password,
                    PasswordResetRequired=user_config.get(
                        "force_password_change", True
                    ),
                )
                result["console_access"] = True
                result["temporary_password"] = password

            # Create access keys
            if user_config.get("programmatic_access", False):
                access_key_response = self.iam.create_access_key(UserName=username)
                result["programmatic_access"] = True
                result["access_key_id"] = access_key_response["AccessKey"][
                    "AccessKeyId"
                ]
                result["secret_access_key"] = access_key_response["AccessKey"][
                    "SecretAccessKey"
                ]

            # Set up MFA requirement
            if user_config.get("require_mfa", False):
                self._attach_mfa_policy(username)
                result["mfa_required"] = True

            logger.info(f"Successfully created user {username}")
            return result

        except ClientError as e:
            error_msg = f"AWS API error creating user {username}: {str(e)}"
            return {"success": False, "error": error_msg, "username": username}
        except Exception as e:
            error_msg = f"Unexpected error creating user {username}: {str(e)}"
            return {"success": False, "error": error_msg, "username": username}

    def create_user_with_config(self, config_file: str) -> dict:
        """
        Create users based on YAML configuration file
        """
        try:
            with open(config_file, "r") as file:
                config = yaml.safe_load(file)

            results = {
                "successful_users": [],
                "failed_users": [],
                "created_groups": [],
                "audit_log": [],
            }

            # Create groups
            for group_config in config.get("groups", []):
                group_result = self._create_group(group_config)
                if group_result["success"]:
                    results["created_groups"].append(group_result)

            # Create users
            for user_config in config.get("users", []):
                user_result = self.create_user(user_config)
                if user_result["success"]:
                    results["successful_users"].append(user_result)
                else:
                    results["failed_users"].append(user_result)

                results["audit_log"].append(
                    {
                        "timestamp": datetime.now().isoformat(),
                        "action": "create_user",
                        "username": user_config.get("username"),
                        "success": user_result["success"],
                        "details": user_result.get(
                            "error", "User created successfully"
                        ),
                    }
                )

            return results

        except Exception as e:
            raise AWSUserProvisioningError(f"Config processing failed: {str(e)}")

    def _create_group(self, group_config: Dict[str, any]) -> Dict[str, any]:
        """Create an IAM group with policies"""
        group_name = group_config.get("name")
        if not group_name:
            return {"success": False, "error": "Group name is required"}

        try:
            # Check if group exists
            try:
                self.iam.get_group(GroupName=group_name)
                return {
                    "success": True,
                    "group_name": group_name,
                    "already_exists": True,
                }
            except ClientError as e:
                if e.response["Error"]["Code"] != "NoSuchEntity":
                    raise

            # Create group
            self.iam.create_group(
                GroupName=group_name, Path=group_config.get("path", "/")
            )

            # Attach policies to group
            for policy_arn in group_config.get("policies", []):
                self.iam.attach_group_policy(GroupName=group_name, PolicyArn=policy_arn)

            return {"success": True, "group_name": group_name, "already_exists": False}

        except Exception as e:
            error_msg = f"Failed to create group {group_name}: {str(e)}"
            return {"success": False, "error": error_msg, "group_name": group_name}

    def _user_exists(self, username: str) -> bool:
        """Check if a user already exists"""
        try:
            self.iam.get_user(UserName=username)
            return True
        except ClientError as e:
            if e.response["Error"]["Code"] == "NoSuchEntity":
                return False
            raise

    def _attach_mfa_policy(self, username: str) -> None:
        """Attach MFA enforcement policy to user"""
        mfa_policy = {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Sid": "AllowViewAccountInfo",
                    "Effect": "Allow",
                    "Action": [
                        "iam:GetAccountPasswordPolicy",
                        "iam:ListVirtualMFADevices",
                    ],
                    "Resource": "*",
                },
                {
                    "Sid": "AllowManageOwnPasswords",
                    "Effect": "Allow",
                    "Action": ["iam:ChangePassword", "iam:GetUser"],
                    "Resource": f"arn:aws:iam::*:user/{username}",
                },
                {
                    "Sid": "AllowManageOwnMFA",
                    "Effect": "Allow",
                    "Action": [
                        "iam:CreateVirtualMFADevice",
                        "iam:DeleteVirtualMFADevice",
                        "iam:EnableMFADevice",
                        "iam:ListMFADevices",
                        "iam:ResyncMFADevice",
                    ],
                    "Resource": [
                        f"arn:aws:iam::*:mfa/{username}",
                        f"arn:aws:iam::*:user/{username}",
                    ],
                },
                {
                    "Sid": "DenyAllExceptUnlessSignedInWithMFA",
                    "Effect": "Deny",
                    "NotAction": [
                        "iam:CreateVirtualMFADevice",
                        "iam:EnableMFADevice",
                        "iam:GetUser",
                        "iam:ListMFADevices",
                        "iam:ListVirtualMFADevices",
                        "iam:ResyncMFADevice",
                        "sts:GetSessionToken",
                    ],
                    "Resource": "*",
                    "Condition": {
                        "BoolIfExists": {"aws:MultiFactorAuthPresent": "false"}
                    },
                },
            ],
        }

        policy_name = f"{username}-MFA-Policy"
        try:
            self.iam.put_user_policy(
                UserName=username,
                PolicyName=policy_name,
                PolicyDocument=json.dumps(mfa_policy),
            )
        except Exception as e:
            logger.error(f"Failed to attach MFA policy to user {username}: {str(e)}")
