from typing import Optional

from pydantic import BaseModel


class OpenSearchPurchaseParams(BaseModel):
    """
    Data class for common parameters.
    https://awscli.amazonaws.com/v2/documentation/api/latest/reference/opensearch/purchase-reserved-instance-offering.html
    """

    region_name: Optional[str] = None
    quantity: Optional[int] = 1
    reservation_name: Optional[str] = None
    purchase_profile: Optional[str] = None


class OpenSearchParams(BaseModel):
    """
    Data class for OpenSearch reserved instance offerings parameters.
    https://boto3.amazonaws.com/v1/documentation/api/1.35.8/reference/services/opensearch/client/describe_reserved_instance_offerings.html
    """

    ReservedInstanceOfferingId: Optional[str] = None
    MaxResults: Optional[int] = 100
    NextToken: Optional[str] = None


class OpenSearchFilterParams(BaseModel):
    """
    Data class for OpenSearch reserved instance offerings filter parameters.
    https://boto3.amazonaws.com/v1/documentation/api/1.35.8/reference/services/opensearch/client/describe_reserved_instance_offerings.html
    """

    ReservedInstanceOfferingId: Optional[str] = None
    InstanceType: Optional[str] = None
    Duration: Optional[int] = 31536000
    CurrencyCode: Optional[str] = "USD"
    PaymentOption: Optional[str] = None
