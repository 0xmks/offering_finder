from typing import Optional, Any, Dict
from pydantic import BaseModel


class RDSPurchaseParams(BaseModel):
    """
    Data class for common parameters.
    https://awscli.amazonaws.com/v2/documentation/api/latest/reference/rds/purchase-reserved-db-instances-offering.html
    """

    purchase_profile: Optional[str] = None
    region_name: Optional[str] = None
    quantity: Optional[int] = 1
    reserved_instance_id: Optional[str] = None


class RDSParams(BaseModel):
    """
    Data class for RDS parameters.
    https://boto3.amazonaws.com/v1/documentation/api/1.35.6/reference/services/rds/client/describe_reserved_db_instances_offerings.html
    """

    ReservedDBInstancesOfferingId: Optional[str] = None
    DBInstanceClass: Optional[str] = None
    Duration: Optional[str] = "31536000"
    ProductDescription: Optional[str] = None
    MultiAZ: Optional[bool] = False
    OfferingType: Optional[str] = None
    MaxRecords: Optional[int] = 100
    Marker: Optional[str] = None
    Filters: Optional[list[Dict[str, Any]]] = None
