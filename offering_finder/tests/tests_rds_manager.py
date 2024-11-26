import unittest
from unittest.mock import patch, MagicMock
from src.offering_finder.managers.rds_manager import OfferingRDSManager
from src.offering_finder.models.rds_params import OfferingParams


class TestOfferingRDSManager(unittest.TestCase):
    @patch("src.offering_finder.clients.rds_client.RDSClient")
    def test_get_offering_ids(self, MockRDSClient):
        # モックの設定
        mock_client = MockRDSClient.return_value
        mock_client.describe_offerings.return_value = {
            "ReservedDBInstancesOfferings": [
                {
                    "ReservedDBInstancesOfferingId": "test-offering-id",
                    "FixedPrice": "100.0",
                }
            ]
        }

        # テスト用のパラメータ
        params = OfferingParams(
            product_description="MySQL",
            db_instance_class="db.m5.large",
            duration="31536000",
            quantity=2,
        )

        manager = OfferingRDSManager(region_name="ap-northeast-1")
        offerings = manager.get_offering_ids(params)

        # 期待される結果
        expected_offering = {
            "ReservedDBInstancesOfferingId": "test-offering-id",
            "FixedPrice": "100.0",
            "OrderQuantity": 2,
            "OrderEstimatedAmount": 200.0,
            "Timestamp": offerings[0][
                "Timestamp"
            ],  # タイムスタンプは動的に生成されるため
        }

        self.assertEqual(len(offerings), 1)
        self.assertDictEqual(offerings[0], expected_offering)


if __name__ == "__main__":
    unittest.main()
