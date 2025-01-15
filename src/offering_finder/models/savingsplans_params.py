from typing import Optional, Any, Dict, List
from pydantic import BaseModel


class SavingsPlansPurchaseParams(BaseModel):
    """
    Data class for common parameters.
    https://awscli.amazonaws.com/v2/documentation/api/latest/reference/savingsplans/create-savings-plan.html
    """

    purchase_profile: Optional[str] = None
    region_name: Optional[str] = None
    offering_id: Optional[str] = None
    commitment: Optional[float] = 0.0
    purchase_time: Optional[str] = None
    client_token: Optional[str] = None
    tags: Optional[List[Dict[str, str]]] = None


class SavingsPlansParams(BaseModel):
    """
    Data class for Savings Plans parameters.
    https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/savingsplans/client/describe_savings_plans_offerings.html
    """

    offeringIds: Optional[List[str]] = None
    paymentOptions: Optional[List[str]] = None
    productType: Optional[str] = None
    planTypes: Optional[List[str]] = None
    durations: Optional[List[int]] = None
    currencies: Optional[List[str]] = None
    descriptions: Optional[List[str]] = None
    serviceCodes: Optional[List[str]] = None
    usageTypes: Optional[List[str]] = None
    operations: Optional[str] = None
    filters: Optional[List[Dict[str, Any]]] = None
    nextToken: Optional[str] = None
    maxResults: Optional[int] = 100
