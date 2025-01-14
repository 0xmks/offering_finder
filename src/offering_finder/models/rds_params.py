from dataclasses import dataclass
from typing import Optional, Dict, Any


@dataclass
class RDSParams:
    """
    Data class for RDS parameters.
    https://docs.aws.amazon.com/AmazonRDS/latest/APIReference/API_DescribeReservedDBInstances.html
    """
    region_name: Optional[str] = "ap-northeast-1"
    quantity: Optional[int] = None
    marker: Optional[str] = None
    reserved_db_instance_id: Optional[str] = None
    reserved_db_instances_offering_id: Optional[str] = None
    db_instance_class: Optional[str] = None
    duration: Optional[str] = None
    offering_type: Optional[str] = None
    multi_az: Optional[bool] = None
    product_description: Optional[str] = None
    filters: Optional[list[Dict[str, Any]]] = None
    max_records: Optional[int] = 100
    reserved_instance_id: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        """
        Converts the parameters to a dictionary for AWS API calls.
        """
        params = {}
        if self.reserved_db_instance_id:
            params["ReservedDBInstanceId"] = self.reserved_db_instance_id
        if self.reserved_db_instances_offering_id:
            params["ReservedDBInstancesOfferingId"] = self.reserved_db_instances_offering_id
        if self.db_instance_class:
            params["DBInstanceClass"] = self.db_instance_class
        if self.duration:
            params["Duration"] = self.duration
        if self.offering_type:
            params["OfferingType"] = self.offering_type
        if self.multi_az is not None:
            params["MultiAZ"] = self.multi_az
        if self.product_description:
            params["ProductDescription"] = self.product_description
        if self.filters:
            params["Filters"] = self.filters
        if self.max_records:
            params["MaxRecords"] = self.max_records
        if self.marker:
            params["Marker"] = self.marker
        return params
