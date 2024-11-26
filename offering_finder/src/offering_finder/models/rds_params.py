from dataclasses import dataclass, field
from typing import Optional, Dict, Any


@dataclass
class OfferingParams:
    reserved_db_instances_offering_id: Optional[str] = None
    product_description: Optional[str] = None
    db_instance_class: Optional[str] = None
    duration: Optional[str] = None
    offering_type: Optional[str] = None
    multi_az: Optional[bool] = None
    quantity: Optional[int] = None
    reserved_instance_id: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        """
        Converts the parameters to a dictionary for AWS API calls.
        """
        params = {}
        if self.reserved_db_instances_offering_id:
            params["ReservedDBInstancesOfferingId"] = (
                self.reserved_db_instances_offering_id
            )
        else:
            if self.product_description:
                params["ProductDescription"] = self.product_description
            if self.db_instance_class:
                params["DBInstanceClass"] = self.db_instance_class
            if self.duration:
                params["Duration"] = self.duration
            if self.offering_type:
                params["OfferingType"] = self.offering_type
            if self.multi_az is not None:
                params["MultiAZ"] = self.multi_az
        return params
