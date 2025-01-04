import datetime
import logging
from typing import Any, Dict, List, Optional
import boto3
from offering_finder.clients.rds_client import RDSClient
from offering_finder.models.rds_params import OfferingParams


class OfferingRDSManager:
    def __init__(self, region_name: str):
        self.client = RDSClient(region_name)

    def add_keys_to_offering(self, offering: Dict[str, Any], params: OfferingParams) -> Dict[str, Any]:
        try:
            if params.quantity:
                offering["OrderQuantity"] = params.quantity
                offering["OrderEstimatedAmount"] = float(offering["FixedPrice"]) * params.quantity
            offering["Timestamp"] = datetime.datetime.now(datetime.timezone.utc).isoformat()
            offering["PurchaseCommand"] = self.generate_purchase_command(
                offering["ReservedDBInstancesOfferingId"],
                params.region_name,
                params.quantity,
                params.reserved_instance_id,
            )
            return offering
        except KeyError as e:
            logging.error(f"Key error: {e}")
        except ValueError as e:
            logging.error(f"Value error: {e}")
        except Exception as e:
            logging.error(f"An unexpected error occurred: {e}")
        return offering

    def get_offering_ids(self, params: OfferingParams) -> List[Dict[str, Any]]:
        try:
            aws_params = params.to_dict()
            result = []
            while True:
                response = self.client.describe_offerings(aws_params)
                offerings = response.get("ReservedDBInstancesOfferings", [])
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

    @staticmethod
    def generate_purchase_command(
        offering_id: str,
        region_name: str,
        quantity: int,
        reserved_instance_id: Optional[str] = None
    ) -> str:
        """
        Generate the AWS CLI command to purchase a reserved DB instance offering.
        """
        command = (
            f"aws rds purchase-reserved-db-instances-offering "
            f"--region {region_name} "
            f"--reserved-db-instances-offering-id {offering_id} "
            f"--db-instance-count {quantity}"
        )
        if reserved_instance_id:
            command += f" --reserved-db-instance-id {reserved_instance_id}"
        return command
