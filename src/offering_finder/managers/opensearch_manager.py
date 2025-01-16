import datetime
import logging
from typing import Any, Dict, List, Optional
import boto3
from offering_finder.clients.AWSClient import AWSClient
from offering_finder.models.opensearch_params import (
    OpenSearchParams,
    OpenSearchFilterParams,
    OpenSearchPurchaseParams,
)


class OpenSearchManager:
    def __init__(self, region_name: str) -> None:
        self.client = AWSClient("opensearch", region_name)

    def generate_purchase_command(
        self,
        offering_id: str,
        region_name: str,
        quantity: int,
        reservation_name: Optional[str] = None,
        purchase_profile: Optional[str] = None,
    ) -> str:
        """
        Generate the AWS CLI command to purchase a reserved instance offering.
        https://docs.aws.amazon.com/cli/latest/reference/opensearch/purchase-reserved-instance-offering.html
        """
        command = ""
        if purchase_profile:
            command += f"AWS_PROFILE={purchase_profile} "
        command += (
            f"aws opensearch purchase-reserved-instance-offering"
            f" --reserved-instance-offering-id {offering_id}"
            f" --instance-count {quantity}"
        )
        if region_name:
            command += f" --region {region_name}"
        if reservation_name:
            command += f" --reservation-name {reservation_name}"
        return command

    def get_offering_ids(self, params: OpenSearchParams) -> List[str]:
        """
        Get the list of OpenSearch reserved instance offering IDs.
        https://boto3.amazonaws.com/v1/documentation/api/1.35.8/reference/services/opensearch/client/describe_reserved_instance_offerings.html
        """
        try:
            fetch_params = params.model_dump(exclude_none=True)
            result = []
            while True:
                response = self.client.describe_offerings(fetch_params)
                offerings = response.get("ReservedInstanceOfferings", [])
                result.extend(offerings)
                if "NextToken" in response:
                    fetch_params["NextToken"] = response["NextToken"]
                else:
                    break
            return result
        except boto3.exceptions.Boto3Error as e:
            logging.error(f"An error occurred: {e}")
            return []

    def filter_offerings(
        self, offerings: List[Dict[str, Any]], params: OpenSearchFilterParams
    ) -> List[Dict[str, Any]]:
        """
        Filter the offerings to match the specified filter parameters.
        """
        result = []
        for offering in offerings:
            if (
                (
                    params.ReservedInstanceOfferingId is None
                    or offering["ReservedInstanceOfferingId"]
                    == params.ReservedInstanceOfferingId
                )
                and (
                    params.InstanceType is None
                    or offering["InstanceType"] == params.InstanceType
                )
                and (
                    params.Duration is None
                    or int(offering["Duration"]) == int(params.Duration)
                )
                and (
                    params.CurrencyCode is None
                    or offering["CurrencyCode"] == params.CurrencyCode
                )
                and (
                    params.PaymentOption is None
                    or offering["PaymentOption"] == params.PaymentOption
                )
            ):
                result.append(offering)
        return result

    def add_keys_to_offerings(
        self, offerings: List[Dict[str, Any]], purchase_params: OpenSearchPurchaseParams
    ) -> List[Dict[str, Any]]:
        result = []
        for offering in offerings:
            try:
                if purchase_params.quantity:
                    offering["OrderQuantity"] = purchase_params.quantity
                    offering["OrderEstimatedAmount"] = (
                        float(offering["FixedPrice"]) * purchase_params.quantity
                    )
                offering["Timestamp"] = datetime.datetime.now(
                    datetime.timezone.utc
                ).isoformat()
                offering["PurchaseCommand"] = self.generate_purchase_command(
                    offering_id=offering["ReservedInstanceOfferingId"],
                    purchase_profile=purchase_params.purchase_profile,
                    region_name=purchase_params.region_name,
                    quantity=purchase_params.quantity,
                    reservation_name=purchase_params.reservation_name,
                )
                result.append(offering)
            except KeyError as e:
                logging.error(f"Key error: {e}")
            except Exception as e:
                logging.error(f"An unexpected error occurred: {e}")
        return result
