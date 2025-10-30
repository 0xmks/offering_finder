import datetime
import logging
from typing import Any, Dict, List
from botocore.exceptions import BotoCoreError, ClientError
from offering_finder.clients.AWSClient import AWSClient
from offering_finder.models.elasticache_params import (
    ElastiCacheParams,
    ElastiCachePurchaseParams,
)


class ElastiCacheManager:
    def __init__(self, region_name: str) -> None:
        self.client = AWSClient("elasticache", region_name)

    def generate_purchase_command(
        self,
        purchase_profile: str,
        region_name: str,
        offering_id: str,
        quantity: int,
        reserved_cache_node_id: str,
    ) -> str:
        """
        Generate the AWS CLI command to purchase a reserved cache node offering.
        """
        command = ""
        if purchase_profile:
            command += f"AWS_PROFILE={purchase_profile} "
        command += (
            f"aws elasticache purchase-reserved-cache-nodes-offering "
            f"--region {region_name} "
            f"--reserved-cache-nodes-offering-id {offering_id} "
            f"--cache-node-count {quantity}"
        )
        if reserved_cache_node_id:
            command += f" --reserved-cache-node-id {reserved_cache_node_id}"
        return command

    def add_keys_to_offerings(
        self, offerings: List[Dict[str, Any]], params: ElastiCachePurchaseParams
    ) -> List[Dict[str, Any]]:
        result = []
        for offering in offerings:
            try:
                offering["OrderQuantity"] = params.quantity
                offering["OrderEstimatedAmount"] = (
                    float(offering["FixedPrice"]) * params.quantity
                )
                offering["Timestamp"] = datetime.datetime.now(
                    datetime.timezone.utc
                ).isoformat()
                offering["PurchaseCommand"] = self.generate_purchase_command(
                    purchase_profile=params.purchase_profile,
                    region_name=params.region_name,
                    offering_id=offering["ReservedCacheNodesOfferingId"],
                    quantity=params.quantity,
                    reserved_cache_node_id=params.reserved_cache_node_id,
                )
                result.append(offering)
            except KeyError as e:
                logging.error(
                    f"Missing required key in offering: {e}, "
                    f"offering_id: {offering.get('ReservedCacheNodesOfferingId', 'unknown')}"
                )
                continue
            except ValueError as e:
                logging.error(
                    f"Invalid value in offering: {e}, "
                    f"offering_id: {offering.get('ReservedCacheNodesOfferingId', 'unknown')}"
                )
                continue
            except Exception as e:
                logging.error(
                    f"Unexpected error processing offering: {e}, "
                    f"offering_id: {offering.get('ReservedCacheNodesOfferingId', 'unknown')}"
                )
                continue
        return result

    def get_offerings(self, params: ElastiCacheParams) -> List[Dict[str, Any]]:
        try:
            fetch_params = params.model_dump(exclude_none=True)
            result = []
            while True:
                response = self.client.describe_offerings(fetch_params)
                offerings = response.get("ReservedCacheNodesOfferings", [])
                result.extend(offerings)
                if "Marker" in response:
                    fetch_params["Marker"] = response["Marker"]
                else:
                    break
            return result
        except ClientError as e:
            error_code = e.response['Error']['Code']
            error_message = e.response['Error']['Message']
            logging.error(f"AWS API Error ({error_code}): {error_message}")
            raise
        except BotoCoreError as e:
            logging.error(f"AWS SDK Error: {e}")
            raise
