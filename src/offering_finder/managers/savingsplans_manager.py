import datetime
import logging
from typing import Any, Dict, List, Optional
from botocore.exceptions import BotoCoreError, ClientError
from offering_finder.clients.AWSClient import AWSClient
from offering_finder.models.savingsplans_params import (
    SavingsPlansParams,
    SavingsPlansPurchaseParams,
)


class SavingsPlansManager:
    def __init__(self, region_name: str) -> None:
        self.client = AWSClient("savingsplans", region_name)

    def generate_purchase_command(
        self,
        purchase_profile: Optional[str],
        region_name: str,
        offering_id: str,
        commitment: int,
        purchase_time: Optional[str] = None,
        client_token: Optional[str] = None,
        tags: Optional[List[Dict[str, str]]] = None,
    ) -> str:
        """
        Generate the AWS CLI command to purchase a reserved cache node offering.
        """
        command = ""
        if purchase_profile:
            command += f"AWS_PROFILE={purchase_profile} "
        command += (
            f"aws savingsplans create-savings-plan"
            f" --region {region_name}"
            f" --savings-plan-offering-id {offering_id}"
            f" --commitment {commitment}"
        )
        if purchase_time:
            command += f" --purchase-time {purchase_time}"
        if client_token:
            command += f" --client-token {client_token}"
        if tags:
            for tag in tags:
                command += f" --tags Key={tag['Key']},Value={tag['Value']}"
        return command

    def add_keys_to_offerings(
        self, offerings: List[Dict[str, Any]], params: SavingsPlansPurchaseParams
    ) -> List[Dict[str, Any]]:
        result = []
        for offering in offerings:
            try:
                offering["OrderCommitment"] = params.commitment
                offering["OrderEstimatedAmount"] = (
                    float(offering["durationSeconds"] / 60 / 60) * params.commitment
                )
                offering["Timestamp"] = datetime.datetime.now(
                    datetime.timezone.utc
                ).isoformat()
                offering["PurchaseCommand"] = self.generate_purchase_command(
                    offering_id=offering["offeringId"],
                    purchase_profile=params.purchase_profile,
                    region_name=params.region_name,
                    commitment=params.commitment,
                    client_token=params.client_token,
                    purchase_time=params.purchase_time,
                    tags=params.tags,
                )
                result.append(offering)
            except KeyError as e:
                logging.error(
                    f"Missing required key in offering: {e}, "
                    f"offering_id: {offering.get('offeringId', 'unknown')}"
                )
                continue
            except ValueError as e:
                logging.error(
                    f"Invalid value in offering: {e}, "
                    f"offering_id: {offering.get('offeringId', 'unknown')}"
                )
                continue
            except Exception as e:
                logging.error(
                    f"Unexpected error processing offering: {e}, "
                    f"offering_id: {offering.get('offeringId', 'unknown')}"
                )
                continue
        return result

    def get_offerings(self, params: SavingsPlansParams) -> List[Dict[str, Any]]:
        try:
            aws_params = params.model_dump(exclude_none=True)
            result = []
            while True:
                response = self.client.describe_offerings(aws_params)
                offerings = response.get("searchResults", [])
                result.extend(offerings)
                if response.get("nextToken"):
                    """ 次ページが無い場合も 'nextToken': '' という形で返ってくるため、空文字ではない事をチェック"""
                    aws_params["nextToken"] = response["nextToken"]
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
