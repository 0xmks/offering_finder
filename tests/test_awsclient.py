import pytest
from unittest.mock import Mock, patch, MagicMock
from src.offering_finder.clients.AWSClient import AWSClient


@patch("src.offering_finder.clients.AWSClient.boto3")
def test_awsclient_init_rds(mock_boto3):
    """RDSサービスのAWSClientが正しく初期化されることを確認"""
    mock_client = Mock()
    mock_boto3.client.return_value = mock_client

    client = AWSClient("rds", "us-west-2")

    mock_boto3.client.assert_called_once_with("rds", region_name="us-west-2")
    assert client.client == mock_client


@patch("src.offering_finder.clients.AWSClient.boto3")
def test_awsclient_init_elasticache(mock_boto3):
    """ElastiCacheサービスのAWSClientが正しく初期化されることを確認"""
    mock_client = Mock()
    mock_boto3.client.return_value = mock_client

    client = AWSClient("elasticache", "us-west-2")

    mock_boto3.client.assert_called_once_with("elasticache", region_name="us-west-2")
    assert client.client == mock_client


@patch("src.offering_finder.clients.AWSClient.boto3")
def test_describe_offerings_rds(mock_boto3):
    """RDSのdescribe_offeringsが正しく呼ばれることを確認"""
    mock_client = Mock()
    mock_client.meta.service_model.service_name = "rds"
    mock_client.describe_reserved_db_instances_offerings.return_value = {
        "ReservedDBInstancesOfferings": [{"OfferingId": "rds-123"}]
    }
    mock_boto3.client.return_value = mock_client

    client = AWSClient("rds", "us-west-2")
    result = client.describe_offerings({"ProductDescription": "MySQL"})

    mock_client.describe_reserved_db_instances_offerings.assert_called_once_with(
        ProductDescription="MySQL"
    )
    assert result == {"ReservedDBInstancesOfferings": [{"OfferingId": "rds-123"}]}


@patch("src.offering_finder.clients.AWSClient.boto3")
def test_describe_offerings_elasticache(mock_boto3):
    """ElastiCacheのdescribe_offeringsが正しく呼ばれることを確認"""
    mock_client = Mock()
    mock_client.meta.service_model.service_name = "elasticache"
    mock_client.describe_reserved_cache_nodes_offerings.return_value = {
        "ReservedCacheNodesOfferings": [{"OfferingId": "ec-123"}]
    }
    mock_boto3.client.return_value = mock_client

    client = AWSClient("elasticache", "us-west-2")
    result = client.describe_offerings({"ProductDescription": "redis"})

    mock_client.describe_reserved_cache_nodes_offerings.assert_called_once_with(
        ProductDescription="redis"
    )
    assert result == {"ReservedCacheNodesOfferings": [{"OfferingId": "ec-123"}]}


@patch("src.offering_finder.clients.AWSClient.boto3")
def test_describe_offerings_savingsplans(mock_boto3):
    """Savings Plansのdescribe_offeringsが正しく呼ばれることを確認"""
    mock_client = Mock()
    mock_client.meta.service_model.service_name = "savingsplans"
    mock_client.describe_savings_plans_offerings.return_value = {
        "searchResults": [{"offeringId": "sp-123"}]
    }
    mock_boto3.client.return_value = mock_client

    client = AWSClient("savingsplans", "us-west-2")
    result = client.describe_offerings({"productType": "EC2"})

    mock_client.describe_savings_plans_offerings.assert_called_once_with(
        productType="EC2"
    )
    assert result == {"searchResults": [{"offeringId": "sp-123"}]}


@patch("src.offering_finder.clients.AWSClient.boto3")
def test_describe_offerings_opensearch(mock_boto3):
    """OpenSearchのdescribe_offeringsが正しく呼ばれることを確認"""
    mock_client = Mock()
    mock_client.meta.service_model.service_name = "opensearch"
    mock_client.describe_reserved_instance_offerings.return_value = {
        "ReservedInstanceOfferings": [{"OfferingId": "os-123"}]
    }
    mock_boto3.client.return_value = mock_client

    client = AWSClient("opensearch", "us-west-2")
    result = client.describe_offerings({"MaxResults": 100})

    mock_client.describe_reserved_instance_offerings.assert_called_once_with(
        MaxResults=100
    )
    assert result == {"ReservedInstanceOfferings": [{"OfferingId": "os-123"}]}


@patch("src.offering_finder.clients.AWSClient.boto3")
def test_describe_offerings_unsupported_service(mock_boto3):
    """未サポートのサービスでValueErrorが発生することを確認"""
    mock_client = Mock()
    mock_client.meta.service_model.service_name = "s3"
    mock_boto3.client.return_value = mock_client

    client = AWSClient("s3", "us-west-2")

    with pytest.raises(ValueError, match="Unsupported service"):
        client.describe_offerings({})


@patch("src.offering_finder.clients.AWSClient.boto3")
def test_describe_offerings_with_multiple_params(mock_boto3):
    """複数のパラメータが正しく渡されることを確認"""
    mock_client = Mock()
    mock_client.meta.service_model.service_name = "rds"
    mock_client.describe_reserved_db_instances_offerings.return_value = {
        "ReservedDBInstancesOfferings": []
    }
    mock_boto3.client.return_value = mock_client

    client = AWSClient("rds", "us-west-2")
    params = {
        "ProductDescription": "MySQL",
        "DBInstanceClass": "db.m5.large",
        "Duration": "31536000",
        "OfferingType": "All Upfront",
    }
    result = client.describe_offerings(params)

    mock_client.describe_reserved_db_instances_offerings.assert_called_once_with(
        **params
    )


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
