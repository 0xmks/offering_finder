import boto3
from typing import Any, Dict


class RDSClient:
    def __init__(self, region_name: str):
        self.client = boto3.client("rds", region_name=region_name)

    def describe_offerings(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Wrapper for AWS describe_reserved_db_instances_offerings API.
        """
        return self.client.describe_reserved_db_instances_offerings(**params)
