import pytest
from src.offering_finder.managers.savingsplans_manager import SavingsPlansManager
from src.offering_finder.models.savingsplans_params import SavingsPlansPurchaseParams


def test_add_keys_to_offerings_single():
    """単一のofferingが正しく処理されることを確認"""
    manager = SavingsPlansManager(region_name="us-west-2")
    offerings = [
        {
            "offeringId": "sp-offering-123",
            "durationSeconds": 31536000,  # 1年 = 8760時間
        }
    ]
    params = SavingsPlansPurchaseParams(
        region_name="us-west-2",
        commitment=10.0,
    )
    result = manager.add_keys_to_offerings(offerings, params)

    assert len(result) == 1
    assert result[0]["OrderCommitment"] == 10.0
    # 31536000秒 = 8760時間、8760 * 10.0 = 87600.0
    assert result[0]["OrderEstimatedAmount"] == 87600.0
    assert "Timestamp" in result[0]
    assert result[0]["PurchaseCommand"] == (
        "aws savingsplans create-savings-plan "
        "--region us-west-2 "
        "--savings-plan-offering-id sp-offering-123 "
        "--commitment 10.0"
    )


def test_add_keys_to_offerings_multiple():
    """複数のofferingsが全て処理されることを確認"""
    manager = SavingsPlansManager(region_name="us-west-2")
    offerings = [
        {
            "offeringId": "sp-offering-1",
            "durationSeconds": 31536000,
        },
        {
            "offeringId": "sp-offering-2",
            "durationSeconds": 94608000,  # 3年
        },
    ]
    params = SavingsPlansPurchaseParams(
        region_name="us-west-2",
        commitment=5.0,
    )
    result = manager.add_keys_to_offerings(offerings, params)

    assert len(result) == 2

    # 1件目の確認
    assert result[0]["offeringId"] == "sp-offering-1"
    assert result[0]["OrderCommitment"] == 5.0
    assert result[0]["OrderEstimatedAmount"] == 43800.0  # 8760 * 5.0

    # 2件目の確認
    assert result[1]["offeringId"] == "sp-offering-2"
    assert result[1]["OrderCommitment"] == 5.0
    assert result[1]["OrderEstimatedAmount"] == 131400.0  # 26280 * 5.0


def test_add_keys_to_offerings_with_purchase_profile():
    """purchase_profileが指定された場合に正しくコマンドに含まれることを確認"""
    manager = SavingsPlansManager(region_name="us-west-2")
    offerings = [
        {
            "offeringId": "sp-offering-123",
            "durationSeconds": 31536000,
        }
    ]
    params = SavingsPlansPurchaseParams(
        purchase_profile="my-profile",
        region_name="us-west-2",
        commitment=10.0,
    )
    result = manager.add_keys_to_offerings(offerings, params)

    assert len(result) == 1
    assert result[0]["PurchaseCommand"].startswith("AWS_PROFILE=my-profile ")


def test_add_keys_to_offerings_with_optional_params():
    """オプションパラメータ（purchase_time, client_token）が正しくコマンドに含まれることを確認"""
    manager = SavingsPlansManager(region_name="us-west-2")
    offerings = [
        {
            "offeringId": "sp-offering-123",
            "durationSeconds": 31536000,
        }
    ]
    params = SavingsPlansPurchaseParams(
        region_name="us-west-2",
        commitment=10.0,
        purchase_time="2025-01-30T00:00:00Z",
        client_token="my-client-token",
    )
    result = manager.add_keys_to_offerings(offerings, params)

    assert len(result) == 1
    assert "--purchase-time 2025-01-30T00:00:00Z" in result[0]["PurchaseCommand"]
    assert "--client-token my-client-token" in result[0]["PurchaseCommand"]


def test_add_keys_to_offerings_with_tags():
    """タグが指定された場合に正しくコマンドに含まれることを確認"""
    manager = SavingsPlansManager(region_name="us-west-2")
    offerings = [
        {
            "offeringId": "sp-offering-123",
            "durationSeconds": 31536000,
        }
    ]
    params = SavingsPlansPurchaseParams(
        region_name="us-west-2",
        commitment=10.0,
        tags=[
            {"Key": "Environment", "Value": "Production"},
            {"Key": "Team", "Value": "DevOps"},
        ],
    )
    result = manager.add_keys_to_offerings(offerings, params)

    assert len(result) == 1
    assert "--tags Key=Environment,Value=Production" in result[0]["PurchaseCommand"]
    assert "--tags Key=Team,Value=DevOps" in result[0]["PurchaseCommand"]


def test_add_keys_to_offerings_empty():
    """空のリストを渡した場合に空のリストが返されることを確認"""
    manager = SavingsPlansManager(region_name="us-west-2")
    offerings = []
    params = SavingsPlansPurchaseParams(
        region_name="us-west-2",
        commitment=10.0,
    )
    result = manager.add_keys_to_offerings(offerings, params)

    assert len(result) == 0


def test_generate_purchase_command():
    """purchase commandの生成が正しく行われることを確認"""
    manager = SavingsPlansManager(region_name="us-west-2")

    # 最小限のパラメータ
    command = manager.generate_purchase_command(
        purchase_profile=None,
        region_name="us-west-2",
        offering_id="sp-offering-123",
        commitment=10,
    )
    assert command == (
        "aws savingsplans create-savings-plan "
        "--region us-west-2 "
        "--savings-plan-offering-id sp-offering-123 "
        "--commitment 10"
    )

    # 全パラメータ指定
    command = manager.generate_purchase_command(
        purchase_profile="my-profile",
        region_name="us-west-2",
        offering_id="sp-offering-123",
        commitment=10,
        purchase_time="2025-01-30T00:00:00Z",
        client_token="token-123",
        tags=[{"Key": "Env", "Value": "Prod"}],
    )
    assert command.startswith("AWS_PROFILE=my-profile ")
    assert "--region us-west-2" in command
    assert "--savings-plan-offering-id sp-offering-123" in command
    assert "--commitment 10" in command
    assert "--purchase-time 2025-01-30T00:00:00Z" in command
    assert "--client-token token-123" in command
    assert "--tags Key=Env,Value=Prod" in command


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
