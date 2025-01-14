from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any


@dataclass
class SavingsPlansParams:
    """
    Data class for Savings Plans parameters.
    https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/savingsplans/client/describe_savings_plans_offerings.html
    """
    region_name: Optional[str] = "ap-northeast-1"
    commitment: Optional[int] = None
    offering_id: Optional[str] = None
    client_token: Optional[str] = None
    payment_options: Optional[List[str]] = field(default_factory=list)
    plan_types: Optional[List[str]] = field(default_factory=list)
    durations: Optional[List[int]] = field(default_factory=list)
    currencies: Optional[List[str]] = field(default_factory=list)
    descriptions: Optional[List[str]] = field(default_factory=list)
    service_codes: Optional[List[str]] = field(default_factory=list)
    usage_types: Optional[List[str]] = field(default_factory=list)
    operations: Optional[List[str]] = field(default_factory=list)
    filters: Optional[List[Dict[str, Any]]] = field(default_factory=list)
    max_results: Optional[int] = 100

    def to_dict(self) -> Dict[str, Any]:
        """
        Converts the parameters to a dictionary for AWS API calls,
        """
        params = {}
        if self.payment_options:
            params["paymentOptions"] = self.payment_options
        if self.plan_types:
            params["planTypes"] = self.plan_types
        if self.durations:
            params["durations"] = self.durations
        if self.currencies:
            params["currencies"] = self.currencies
        if self.currencies:
            params["descriptions"] = self.descriptions
        if self.service_codes:
            params["serviceCodes"] = self.service_codes
        if self.usage_types:
            params["usageTypes"] = self.usage_types
        if self.operations:
            params["operations"] = self.operations
        if self.filters:
            params["filters"] = self.filters
        if self.max_results:
            params["maxResults"] = self.max_results
        return params
