from typing import Optional
from pydantic import BaseModel


class ElastiCachePurchaseParams(BaseModel):
    """
    Data class for common parameters.
    https://awscli.amazonaws.com/v2/documentation/api/latest/reference/elasticache/purchase-reserved-cache-nodes-offering.html
    """

    purchase_profile: Optional[str] = None
    region_name: Optional[str] = None
    quantity: Optional[int] = 1
    reserved_cache_node_id: Optional[str] = None


class ElastiCacheParams(BaseModel):
    """
    Data class for ElastiCache parameters.
    https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticache/client/describe_reserved_cache_nodes_offerings.html
    """

    ReservedCacheNodesOfferingId: Optional[str] = None
    CacheNodeType: Optional[str] = None
    Duration: Optional[str] = "31536000"
    ProductDescription: Optional[str] = None
    OfferingType: Optional[str] = "All Upfront"
    MaxRecords: Optional[int] = 100
    Marker: Optional[str] = None
