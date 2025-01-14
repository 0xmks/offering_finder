import datetime
import logging
from typing import Any, Dict, List, Optional
import boto3
from offering_finder.clients.AWSClient import AWSClient
from offering_finder.models.savingsplans_params import SavingsPlansParams


class SavingsPlansManager:
    def __init__(
        self,
        region_name: str
    ) -> None:
        self.client = AWSClient("savingsplans", region_name)

    def generate_purchase_command(
        self,
        offering_id: str,
        region_name: str,
        commitment: int,
        client_token: Optional[str] = None
    ) -> str:
        """
        Generate the AWS CLI command to purchase a reserved cache node offering.
        """
        command = (
            f"aws savingsplans create-savings-plan "
            f"--region {region_name} "
            f"--savings-plan-offering-id {offering_id} "
            f"--commitment {commitment}"
        )
        if client_token:
            command += f" --client-token {client_token}"
        return command

    def add_keys_to_offering(
            self,
            offering: Dict[str, Any],
            params: SavingsPlansParams
    ) -> Dict[str, Any]:
        try:
            if params.commitment:
                offering["OrderCommitment"] = params.commitment
                offering["OrderEstimatedAmount"] = float(offering["durationSeconds"]) * params.commitment
            offering["Timestamp"] = datetime.datetime.now(datetime.timezone.utc).isoformat()
            offering["PurchaseCommand"] = self.generate_purchase_command(
                offering["offeringId"],
                params.region_name,
                params.commitment,
                params.client_token,
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
            params: SavingsPlansParams
    ) -> List[Dict[str, Any]]:
        try:
            aws_params = params.to_dict()
            result = []
            while True:
                response = self.client.describe_offerings(aws_params)
                offerings = response.get("searchResults", [])
                for offering in offerings:
                    offering = self.add_keys_to_offering(offering, params)
                result.extend(offerings)
                if response.get("nextToken"):
                    """ 次ページが無い場合も 'nextToken': '' という形で返ってくるため、空文字ではない事をチェックする"""
                    aws_params["nextToken"] = response["nextToken"]
                else:
                    break
            return result
        except boto3.exceptions.Boto3Error as e:
            logging.error(f"An error occurred: {e}")
            return []
