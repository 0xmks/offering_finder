from dataclasses import dataclass, asdict, field
from typing import Optional, Dict, Any
import datetime

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
class OpenSearchReservedInstance:
    """
    Data class for OpenSearch reserved instance offerings.
    """
    offering_id: str
    instance_type: str
    duration: str
    fixed_price: float
    usage_price: float
    currency_code: str
    payment_option: str
    offering_type: str
    region: str
    timestamp: str = field(init=False)
