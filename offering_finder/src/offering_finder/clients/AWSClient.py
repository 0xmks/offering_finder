import boto3
from typing import Any, Dict


class AWSClient:
    def __init__(
            self, 
            service_name: str, 
            region_name: str
    ) -> None:
        self.client = boto3.client(service_name, region_name=region_name)

    def describe_offerings(
            self, 
            params: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Wrapper for AWS describe_reserved_db_instances_offerings or describe_reserved_cache_nodes_offerings API.
        """
        if self.client.meta.service_model.service_name == "rds":
            return self.client.describe_reserved_db_instances_offerings(**params)
        elif self.client.meta.service_model.service_name == "elasticache":
            return self.client.describe_reserved_cache_nodes_offerings(**params)
        else:
            raise ValueError("Unsupported service")
