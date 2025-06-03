"""This util module contains the logger configuration for AWS user provisioning."""

import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("aws_user_provisioning.log"),
        logging.StreamHandler(),
    ],
)
logger = logging.getLogger(__name__)
