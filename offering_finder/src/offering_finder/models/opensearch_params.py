from dataclasses import dataclass
from typing import Optional, Dict, Any

@dataclass
class OpenSearchPurchaseParams:
    """
    Data class for common parameters.
    """
    region_name: Optional[str] = "ap-northeast-1"
    quantity: Optional[int] = 1
    reservation_name: Optional[str] = None

@dataclass
class OpenSearchParams:
    """
    Data class for OpenSearch reserved instance offerings parameters.
    https://boto3.amazonaws.com/v1/documentation/api/1.35.8/reference/services/opensearch/client/describe_reserved_instance_offerings.html
    """
    reserved_instance_offering_id: Optional[str] = None
    max_results: Optional[int] = 100
    next_token: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        """
        Converts the parameters to a dictionary for AWS API calls.
        """
        params = {}
        if self.reserved_instance_offering_id:
            params["ReservedInstanceOfferingId"] = self.reserved_instance_offering_id
        if self.max_results:
            params["MaxResults"] = self.max_results
        if self.next_token:
            params["NextToken"] = self.next_token
        return params

@dataclass
class OpenSearchFilterParams:
    """
    Data class for OpenSearch reserved instance offerings filter parameters.
    https://boto3.amazonaws.com/v1/documentation/api/1.35.8/reference/services/opensearch/client/describe_reserved_instance_offerings.html
    """
    reserved_instance_offering_id: Optional[str] = None
    instance_type: Optional[str] = None
    duration: Optional[int] = None
    currency_code: Optional[str] = None
    payment_option: Optional[str] = None
