import pytest
from src.offering_finder.managers.rds_manager import RDSManager
from src.offering_finder.models.rds_params import RDSPurchaseParams


def test_add_keys_to_offerings_single():
    """単一のofferingが正しく処理されることを確認"""
    manager = RDSManager(region_name="ap-northeast-1")
    offerings = [
        {
            "ReservedDBInstancesOfferingId": "offering-id-123",
            "FixedPrice": 100.0
        }
    ]
    params = RDSPurchaseParams(
        region_name="ap-northeast-1",
        quantity=2,
        reserved_instance_id=None
    )
    result = manager.add_keys_to_offerings(offerings, params)

    assert len(result) == 1
    assert result[0]["OrderQuantity"] == 2
    assert result[0]["OrderEstimatedAmount"] == 200.0
    assert "Timestamp" in result[0]
    assert result[0]["PurchaseCommand"] == (
        "aws rds purchase-reserved-db-instances-offering "
        "--region ap-northeast-1 "
        "--reserved-db-instances-offering-id offering-id-123 "
        "--db-instance-count 2"
    )


def test_add_keys_to_offerings_multiple():
    """複数のofferingsが全て処理されることを確認（バグ修正の確認）"""
    manager = RDSManager(region_name="ap-northeast-1")
    offerings = [
        {
            "ReservedDBInstancesOfferingId": "offering-id-1",
            "FixedPrice": 100.0
        },
        {
            "ReservedDBInstancesOfferingId": "offering-id-2",
            "FixedPrice": 200.0
        },
        {
            "ReservedDBInstancesOfferingId": "offering-id-3",
            "FixedPrice": 300.0
        }
    ]
    params = RDSPurchaseParams(
        region_name="ap-northeast-1",
        quantity=3,
        reserved_instance_id=None
    )
    result = manager.add_keys_to_offerings(offerings, params)

    # バグ修正前は1件しか返されなかったが、修正後は全て処理される
    assert len(result) == 3

    # 1件目の確認
    assert result[0]["ReservedDBInstancesOfferingId"] == "offering-id-1"
    assert result[0]["OrderQuantity"] == 3
    assert result[0]["OrderEstimatedAmount"] == 300.0

    # 2件目の確認
    assert result[1]["ReservedDBInstancesOfferingId"] == "offering-id-2"
    assert result[1]["OrderQuantity"] == 3
    assert result[1]["OrderEstimatedAmount"] == 600.0

    # 3件目の確認
    assert result[2]["ReservedDBInstancesOfferingId"] == "offering-id-3"
    assert result[2]["OrderQuantity"] == 3
    assert result[2]["OrderEstimatedAmount"] == 900.0


def test_add_keys_to_offerings_with_reserved_instance_id():
    """reserved_instance_idが指定された場合に正しくコマンドに含まれることを確認"""
    manager = RDSManager(region_name="ap-northeast-1")
    offerings = [
        {
            "ReservedDBInstancesOfferingId": "offering-id-123",
            "FixedPrice": 100.0
        }
    ]
    params = RDSPurchaseParams(
        region_name="ap-northeast-1",
        quantity=2,
        reserved_instance_id="my-reserved-instance"
    )
    result = manager.add_keys_to_offerings(offerings, params)

    assert len(result) == 1
    assert result[0]["PurchaseCommand"] == (
        "aws rds purchase-reserved-db-instances-offering "
        "--region ap-northeast-1 "
        "--reserved-db-instances-offering-id offering-id-123 "
        "--db-instance-count 2 "
        "--reserved-db-instance-id my-reserved-instance"
    )


def test_add_keys_to_offerings_with_purchase_profile():
    """purchase_profileが指定された場合に正しくコマンドに含まれることを確認"""
    manager = RDSManager(region_name="ap-northeast-1")
    offerings = [
        {
            "ReservedDBInstancesOfferingId": "offering-id-123",
            "FixedPrice": 100.0
        }
    ]
    params = RDSPurchaseParams(
        purchase_profile="my-profile",
        region_name="ap-northeast-1",
        quantity=2,
        reserved_instance_id=None
    )
    result = manager.add_keys_to_offerings(offerings, params)

    assert len(result) == 1
    assert result[0]["PurchaseCommand"].startswith("AWS_PROFILE=my-profile ")


def test_add_keys_to_offerings_empty():
    """空のリストを渡した場合に空のリストが返されることを確認"""
    manager = RDSManager(region_name="ap-northeast-1")
    offerings = []
    params = RDSPurchaseParams(
        region_name="ap-northeast-1",
        quantity=1
    )
    result = manager.add_keys_to_offerings(offerings, params)

    assert len(result) == 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
