import pytest
from src.offering_finder.managers.elasticache_manager import ElastiCacheManager
from src.offering_finder.models.elasticache_params import ElastiCacheParams
from unittest.mock import MagicMock

def test_add_keys_to_offering_success():
    manager = ElastiCacheManager(region_name="us-west-2")
    offering = {
        "ReservedCacheNodesOfferingId": "offering-id-123",
        "FixedPrice": "100.0"
    }
    params = ElastiCacheParams(
        region_name="us-west-2",
        quantity=2,
        reserved_cache_node_id=None
    )
    updated_offering = manager.add_keys_to_offering(offering, params)
    assert updated_offering["OrderQuantity"] == 2
    assert updated_offering["OrderEstimatedAmount"] == 200.0
    assert "Timestamp" in updated_offering
    assert updated_offering["PurchaseCommand"] == (
        "aws elasticache purchase-reserved-cache-nodes-offering "
        "--region us-west-2 "
        "--reserved-cache-nodes-offering-id offering-id-123 "
        "--cache-node-count 2"
    )

def test_add_keys_to_offering_with_reserved_cache_node_id():
    manager = ElastiCacheManager(region_name="us-west-2")
    offering = {
        "ReservedCacheNodesOfferingId": "offering-id-123",
        "FixedPrice": "100.0"
    }
    params = ElastiCacheParams(
        region_name="us-west-2",
        quantity=2,
        reserved_cache_node_id="node-id-123"
    )
    updated_offering = manager.add_keys_to_offering(offering, params)
    assert updated_offering["OrderQuantity"] == 2
    assert updated_offering["OrderEstimatedAmount"] == 200.0
    assert "Timestamp" in updated_offering
    assert updated_offering["PurchaseCommand"] == (
        "aws elasticache purchase-reserved-cache-nodes-offering "
        "--region us-west-2 "
        "--reserved-cache-nodes-offering-id offering-id-123 "
        "--cache-node-count 2 "
        "--reserved-cache-node-id node-id-123"
    )

if __name__ == "__main__":
    pytest.main()
