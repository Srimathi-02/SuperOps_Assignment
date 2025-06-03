"""Main module for the AWS User Provisioning application."""

from services.services import AWSUserProvisioner
import yaml
import json
from datetime import datetime
from pathlib import Path

from utils.logger import logger


def main():
    """
    Main function demonstrating the usage of AWSUserProvisioner
    """
    # Load configuration from YAML file
    config_file = "user_config.yaml"
    try:
        with open(config_file, "r") as f:
            yaml.safe_load(f)
    except FileNotFoundError:
        logger.error(f"Configuration file {config_file} not found.")
        return

    try:
        provisioner = AWSUserProvisioner()

        results = provisioner.create_user_with_config(config_file)

        print("\n=== Summary ===")
        print(f"Successfully created {len(results['successful_users'])} users")
        print(f"Failed to create {len(results['failed_users'])} users")
        print(f"Created {len(results['created_groups'])} groups")

        for user in results["successful_users"]:
            print(f"\nUser: {user['username']}")
            print(f"  ARN: {user['user_arn']}")
            print(f"  Console Access: {user['console_access']}")
            print(f"  Programmatic Access: {user['programmatic_access']}")
            if user.get("temporary_password"):
                print(f"  Temporary Password: {user['temporary_password']}")
            if user.get("access_key_id"):
                print(f"  Access Key ID: {user['access_key_id']}")

        audit_log_file = Path(
            f"logs/audit_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        )
        audit_log_file.parent.mkdir(parents=True, exist_ok=True)
        with open(audit_log_file, "w") as f:
            json.dump(results["audit_log"], f, indent=2)
        logger.info(f"Audit log saved to {audit_log_file}")

    except Exception as e:
        logger.error(f"Main execution failed: {str(e)}")
        print(f"Error: {str(e)}")


if __name__ == "__main__":
    main()
