import datetime
import logging
from typing import Any, Dict, List, Optional
import boto3
from offering_finder.clients.AWSClient import AWSClient
from offering_finder.models.elasticache_params import ElastiCacheParams


class ElastiCacheManager:
    def __init__(
        self, 
        region_name: str
    ) -> None:
        self.client = AWSClient("elasticache",region_name)

    def generate_purchase_command(
        self,
        offering_id: str,
        region_name: str,
        quantity: int,
        reserved_cache_node_id: Optional[str] = None
    ) -> str:
        """
        Generate the AWS CLI command to purchase a reserved cache node offering.
        """
        command = (
            f"aws elasticache purchase-reserved-cache-nodes-offering "
            f"--region {region_name} "
            f"--reserved-cache-nodes-offering-id {offering_id} "
            f"--cache-node-count {quantity}"
        )
        if reserved_cache_node_id:
            command += f" --reserved-cache-node-id {reserved_cache_node_id}"
        return command

    def add_keys_to_offering(
            self, 
            offering: Dict[str, Any], 
            params: ElastiCacheParams
    ) -> Dict[str, Any]:
        try:
            if params.quantity:
                offering["OrderQuantity"] = params.quantity
                offering["OrderEstimatedAmount"] = float(offering["FixedPrice"]) * params.quantity
            offering["Timestamp"] = datetime.datetime.now(datetime.timezone.utc).isoformat()
            offering["PurchaseCommand"] = self.generate_purchase_command(
                offering["ReservedCacheNodesOfferingId"],
                params.region_name,
                params.quantity,
                params.reserved_cache_node_id,
            )
            return offering
        except KeyError as e:
            logging.error(f"Key error: {e}")
        except ValueError as e:
            logging.error(f"Value error: {e}")
        except Exception as e:
            logging.error(f"An unexpected error occurred: {e}")
        return offering

    def get_offering_ids(
            self, 
            params: ElastiCacheParams
    ) -> List[Dict[str, Any]]:
        try:
            aws_params = params.to_dict()
            result = []
            while True:
                response = self.client.describe_offerings(aws_params)
                offerings = response.get("ReservedCacheNodesOfferings", [])
                for offering in offerings:
                    offering = self.add_keys_to_offering(offering, params)
                result.extend(offerings)
                if "Marker" in response:
                    aws_params["Marker"] = response["Marker"]
                else:
                    break
            return result
        except boto3.exceptions.Boto3Error as e:
            logging.error(f"An error occurred: {e}")
            return []
