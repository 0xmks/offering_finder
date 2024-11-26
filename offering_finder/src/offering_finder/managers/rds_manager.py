import datetime
import logging
from typing import Any, Dict, List, Optional
import boto3
from offering_finder.clients.rds_client import RDSClient
from offering_finder.models.rds_params import OfferingParams


class OfferingRDSManager:
    def __init__(self, region_name: str):
        self.client = RDSClient(region_name)

    def get_offering_ids(self, params: OfferingParams) -> List[Dict[str, Any]]:
        try:
            aws_params = params.to_dict()
            result = []
            while True:
                response = self.client.describe_offerings(aws_params)
                offerings = response.get("ReservedDBInstancesOfferings", [])
                for offering in offerings:
                    if params.quantity:
                        offering["OrderQuantity"] = params.quantity
                        offering["OrderEstimatedAmount"] = (
                            float(offering["FixedPrice"]) * params.quantity
                        )
                    offering["Timestamp"] = datetime.datetime.now(
                        datetime.timezone.utc
                    ).isoformat()
                    # CLIコマンド情報を追加
                    offering["PurchaseCommand"] = self.generate_purchase_command(
                        offering["ReservedDBInstancesOfferingId"],
                        params.quantity,
                        params.reserved_instance_id,
                    )
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
        offering_id: str, quantity: int, reserved_instance_id: Optional[str] = None
    ) -> str:
        """
        Generate the AWS CLI command to purchase a reserved DB instance offering.
        """
        command = (
            f"aws rds purchase-reserved-db-instances-offering "
            f"--reserved-db-instances-offering-id {offering_id} "
            f"--db-instance-count {quantity}"
        )
        if reserved_instance_id:
            command += f" --reserved-db-instance-id {reserved_instance_id}"
        return command
