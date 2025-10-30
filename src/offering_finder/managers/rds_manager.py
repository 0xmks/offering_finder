import datetime
import logging
from typing import Any, Dict, List, Optional
import boto3
from offering_finder.clients.AWSClient import AWSClient
from offering_finder.models.rds_params import RDSParams, RDSPurchaseParams


class RDSManager:
    def __init__(self, region_name: str) -> None:
        self.client = AWSClient("rds", region_name)

    def generate_purchase_command(
        self,
        purchase_profile: Optional[str],
        offering_id: str,
        region_name: str,
        quantity: int,
        reserved_instance_id: Optional[str] = None,
    ) -> str:
        """
        Generate the AWS CLI command to purchase a reserved DB instance offering.
        """
        command = ""
        if purchase_profile:
            command += f"AWS_PROFILE={purchase_profile} "
        command += (
            f"aws rds purchase-reserved-db-instances-offering "
            f"--region {region_name} "
            f"--reserved-db-instances-offering-id {offering_id} "
            f"--db-instance-count {quantity}"
        )
        if reserved_instance_id:
            command += f" --reserved-db-instance-id {reserved_instance_id}"
        return command

    def add_keys_to_offerings(
        self, offerings: List[Dict[str, Any]], params: RDSPurchaseParams
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
                    offering_id=offering["ReservedDBInstancesOfferingId"],
                    quantity=params.quantity,
                    reserved_instance_id=params.reserved_instance_id,
                )
                result.append(offering)
            except KeyError as e:
                logging.error(f"Key error: {e}")
            except ValueError as e:
                logging.error(f"Value error: {e}")
            except Exception as e:
                logging.error(f"An unexpected error occurred: {e}")
        return result

    def get_offerings(self, params: RDSParams) -> List[Dict[str, Any]]:
        try:
            rds_params = params.model_dump(exclude_none=True)
            result = []
            while True:
                response = self.client.describe_offerings(rds_params)
                offerings = response.get("ReservedDBInstancesOfferings", [])
                result.extend(offerings)
                if "Marker" in response:
                    rds_params["Marker"] = response["Marker"]
                else:
                    break
            return result
        except boto3.exceptions.Boto3Error as e:
            logging.error(f"An error occurred: {e}")
            return []
