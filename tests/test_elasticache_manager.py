import pytest
from src.offering_finder.managers.elasticache_manager import ElastiCacheManager
from src.offering_finder.models.elasticache_params import ElastiCachePurchaseParams

def test_add_keys_to_offering_success():
    manager = ElastiCacheManager(region_name="us-west-2")
    offerings = [
        {
            "ReservedCacheNodesOfferingId": "offering-id-123",
            "FixedPrice": 100.0
        }
    ]
    params = ElastiCachePurchaseParams(
        region_name="us-west-2",
        quantity=2,
        reserved_cache_node_id=None
    )
    result = manager.add_keys_to_offerings(offerings, params)
    assert len(result) == 1
    assert result[0]["OrderQuantity"] == 2
    assert result[0]["OrderEstimatedAmount"] == 200.0
    assert "Timestamp" in result[0]
    assert result[0]["PurchaseCommand"] == (
        "aws elasticache purchase-reserved-cache-nodes-offering "
        "--region us-west-2 "
        "--reserved-cache-nodes-offering-id offering-id-123 "
        "--cache-node-count 2"
    )

def test_add_keys_to_offering_with_reserved_cache_node_id():
    manager = ElastiCacheManager(region_name="us-west-2")
    offerings = [
        {
            "ReservedCacheNodesOfferingId": "offering-id-123",
            "FixedPrice": 100.0
        }
    ]
    params = ElastiCachePurchaseParams(
        region_name="us-west-2",
        quantity=2,
        reserved_cache_node_id="node-id-123"
    )
    result = manager.add_keys_to_offerings(offerings, params)
    assert len(result) == 1
    assert result[0]["OrderQuantity"] == 2
    assert result[0]["OrderEstimatedAmount"] == 200.0
    assert "Timestamp" in result[0]
    assert result[0]["PurchaseCommand"] == (
        "aws elasticache purchase-reserved-cache-nodes-offering "
        "--region us-west-2 "
        "--reserved-cache-nodes-offering-id offering-id-123 "
        "--cache-node-count 2 "
        "--reserved-cache-node-id node-id-123"
    )

if __name__ == "__main__":
    pytest.main()
