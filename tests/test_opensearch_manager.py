import pytest
from src.offering_finder.managers.opensearch_manager import OpenSearchManager
from src.offering_finder.models.opensearch_params import (
    OpenSearchPurchaseParams,
    OpenSearchFilterParams,
)


def test_add_keys_to_offerings_single():
    """単一のofferingが正しく処理されることを確認"""
    manager = OpenSearchManager(region_name="us-west-2")
    offerings = [
        {
            "ReservedInstanceOfferingId": "offering-id-123",
            "FixedPrice": 100.0,
        }
    ]
    params = OpenSearchPurchaseParams(
        region_name="us-west-2",
        quantity=2,
    )
    result = manager.add_keys_to_offerings(offerings, params)

    assert len(result) == 1
    assert result[0]["OrderQuantity"] == 2
    assert result[0]["OrderEstimatedAmount"] == 200.0
    assert "Timestamp" in result[0]
    assert result[0]["PurchaseCommand"] == (
        "aws opensearch purchase-reserved-instance-offering "
        "--reserved-instance-offering-id offering-id-123 "
        "--instance-count 2 "
        "--region us-west-2"
    )


def test_add_keys_to_offerings_multiple():
    """複数のofferingsが全て処理されることを確認"""
    manager = OpenSearchManager(region_name="us-west-2")
    offerings = [
        {
            "ReservedInstanceOfferingId": "offering-id-1",
            "FixedPrice": 100.0,
        },
        {
            "ReservedInstanceOfferingId": "offering-id-2",
            "FixedPrice": 200.0,
        },
        {
            "ReservedInstanceOfferingId": "offering-id-3",
            "FixedPrice": 300.0,
        },
    ]
    params = OpenSearchPurchaseParams(
        region_name="us-west-2",
        quantity=3,
    )
    result = manager.add_keys_to_offerings(offerings, params)

    assert len(result) == 3

    # 1件目の確認
    assert result[0]["ReservedInstanceOfferingId"] == "offering-id-1"
    assert result[0]["OrderQuantity"] == 3
    assert result[0]["OrderEstimatedAmount"] == 300.0

    # 2件目の確認
    assert result[1]["ReservedInstanceOfferingId"] == "offering-id-2"
    assert result[1]["OrderQuantity"] == 3
    assert result[1]["OrderEstimatedAmount"] == 600.0

    # 3件目の確認
    assert result[2]["ReservedInstanceOfferingId"] == "offering-id-3"
    assert result[2]["OrderQuantity"] == 3
    assert result[2]["OrderEstimatedAmount"] == 900.0


def test_add_keys_to_offerings_with_reservation_name():
    """reservation_nameが指定された場合に正しくコマンドに含まれることを確認"""
    manager = OpenSearchManager(region_name="us-west-2")
    offerings = [
        {
            "ReservedInstanceOfferingId": "offering-id-123",
            "FixedPrice": 100.0,
        }
    ]
    params = OpenSearchPurchaseParams(
        region_name="us-west-2",
        quantity=2,
        reservation_name="my-reservation",
    )
    result = manager.add_keys_to_offerings(offerings, params)

    assert len(result) == 1
    assert result[0]["PurchaseCommand"] == (
        "aws opensearch purchase-reserved-instance-offering "
        "--reserved-instance-offering-id offering-id-123 "
        "--instance-count 2 "
        "--region us-west-2 "
        "--reservation-name my-reservation"
    )


def test_add_keys_to_offerings_with_purchase_profile():
    """purchase_profileが指定された場合に正しくコマンドに含まれることを確認"""
    manager = OpenSearchManager(region_name="us-west-2")
    offerings = [
        {
            "ReservedInstanceOfferingId": "offering-id-123",
            "FixedPrice": 100.0,
        }
    ]
    params = OpenSearchPurchaseParams(
        purchase_profile="my-profile",
        region_name="us-west-2",
        quantity=2,
    )
    result = manager.add_keys_to_offerings(offerings, params)

    assert len(result) == 1
    assert result[0]["PurchaseCommand"].startswith("AWS_PROFILE=my-profile ")


def test_add_keys_to_offerings_empty():
    """空のリストを渡した場合に空のリストが返されることを確認"""
    manager = OpenSearchManager(region_name="us-west-2")
    offerings = []
    params = OpenSearchPurchaseParams(
        region_name="us-west-2",
        quantity=1,
    )
    result = manager.add_keys_to_offerings(offerings, params)

    assert len(result) == 0


def test_filter_offerings_match_all():
    """全ての条件に一致するofferingが正しくフィルタリングされることを確認"""
    manager = OpenSearchManager(region_name="us-west-2")
    offerings = [
        {
            "ReservedInstanceOfferingId": "offering-1",
            "InstanceType": "m5.large",
            "Duration": 31536000,
            "CurrencyCode": "USD",
            "PaymentOption": "ALL_UPFRONT",
        },
        {
            "ReservedInstanceOfferingId": "offering-2",
            "InstanceType": "m5.xlarge",
            "Duration": 31536000,
            "CurrencyCode": "USD",
            "PaymentOption": "ALL_UPFRONT",
        },
    ]
    filter_params = OpenSearchFilterParams(
        InstanceType="m5.large",
        Duration=31536000,
        CurrencyCode="USD",
        PaymentOption="ALL_UPFRONT",
    )
    result = manager.filter_offerings(offerings, filter_params)

    assert len(result) == 1
    assert result[0]["ReservedInstanceOfferingId"] == "offering-1"


def test_filter_offerings_no_match():
    """条件に一致しないofferingがフィルタリングされることを確認"""
    manager = OpenSearchManager(region_name="us-west-2")
    offerings = [
        {
            "ReservedInstanceOfferingId": "offering-1",
            "InstanceType": "m5.large",
            "Duration": 31536000,
            "CurrencyCode": "USD",
            "PaymentOption": "ALL_UPFRONT",
        },
    ]
    filter_params = OpenSearchFilterParams(
        InstanceType="m5.xlarge",  # 一致しない
    )
    result = manager.filter_offerings(offerings, filter_params)

    assert len(result) == 0


def test_filter_offerings_partial_match():
    """一部の条件のみ指定した場合に正しくフィルタリングされることを確認"""
    manager = OpenSearchManager(region_name="us-west-2")
    offerings = [
        {
            "ReservedInstanceOfferingId": "offering-1",
            "InstanceType": "m5.large",
            "Duration": 31536000,
            "CurrencyCode": "USD",
            "PaymentOption": "ALL_UPFRONT",
        },
        {
            "ReservedInstanceOfferingId": "offering-2",
            "InstanceType": "m5.large",
            "Duration": 31536000,  # デフォルト値と同じにする
            "CurrencyCode": "USD",
            "PaymentOption": "NO_UPFRONT",
        },
    ]
    filter_params = OpenSearchFilterParams(
        InstanceType="m5.large",
        # Duration と CurrencyCode はデフォルト値を使用
        # PaymentOption は None
    )
    result = manager.filter_offerings(offerings, filter_params)

    # m5.large で Duration が 31536000 (デフォルト), CurrencyCode が USD (デフォルト) の両方が一致
    assert len(result) == 2


def test_generate_purchase_command():
    """purchase commandの生成が正しく行われることを確認"""
    manager = OpenSearchManager(region_name="us-west-2")

    # 最小限のパラメータ
    command = manager.generate_purchase_command(
        offering_id="offering-123",
        region_name="us-west-2",
        quantity=2,
    )
    assert command == (
        "aws opensearch purchase-reserved-instance-offering "
        "--reserved-instance-offering-id offering-123 "
        "--instance-count 2 "
        "--region us-west-2"
    )

    # 全パラメータ指定
    command = manager.generate_purchase_command(
        offering_id="offering-123",
        region_name="us-west-2",
        quantity=2,
        reservation_name="my-reservation",
        purchase_profile="my-profile",
    )
    assert command.startswith("AWS_PROFILE=my-profile ")
    assert "--reserved-instance-offering-id offering-123" in command
    assert "--instance-count 2" in command
    assert "--region us-west-2" in command
    assert "--reservation-name my-reservation" in command


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
