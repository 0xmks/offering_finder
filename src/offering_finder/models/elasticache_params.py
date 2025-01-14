from dataclasses import dataclass
from typing import Optional, Dict, Any


@dataclass
class ElastiCacheParams:
    """
    Data class for ElastiCache parameters.
    https://docs.aws.amazon.com/AmazonElastiCache/latest/APIReference/API_DescribeReservedCacheNodes.html
    """
    region_name: Optional[str] = "ap-northeast-1"
    quantity: Optional[int] = 1
    marker: Optional[str] = None
    reserved_cache_nodes_offering_id: Optional[str] = None
    cache_node_type: Optional[str] = None
    duration: Optional[str] = '31536000'
    product_description: Optional[str] = None
    offering_type: Optional[str] = 'All Upfront'
    max_records: Optional[int] = 100
    reserved_cache_node_id: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        """
        Converts the parameters to a dictionary for AWS API calls.
        """
        params = {}
        if self.reserved_cache_nodes_offering_id:
            params["ReservedCacheNodesOfferingId"] = self.reserved_cache_nodes_offering_id
        if self.cache_node_type:
            params["CacheNodeType"] = self.cache_node_type
        if self.duration:
            params["Duration"] = self.duration
        if self.product_description:
            params["ProductDescription"] = self.product_description
        if self.offering_type:
            params["OfferingType"] = self.offering_type
        if self.max_records:
            params["MaxRecords"] = self.max_records
        if self.marker:
            params["Marker"] = self.marker
        return params
