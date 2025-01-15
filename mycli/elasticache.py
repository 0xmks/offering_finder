import click
import json
from src.offering_finder.models.elasticache_params import (
    ElastiCacheParams,
    ElastiCachePurchaseParams,
)
from src.offering_finder.managers.elasticache_manager import ElastiCacheManager


# elasticache subcommand
@click.command()
@click.option(
    "--purchase_profile",
    required=False,
    type=str,
    help="Purchase command set a named profile (e.g., 'default' 'my-profile')",
)
@click.option(
    "--region_name", required=True, help="AWS region name (e.g., 'ap-northeast-1')"
)
@click.option("--quantity", required=True, type=int, help="Quantity (e.g., 1)")
@click.option(
    "--cache_node_type",
    required=True,
    type=str,
    help=(
        "Cache node type "
        "(e.g., 'cache.m5.large' 'cache.r5.xlarge' 'cache.t3.medium'...)"
    ),
)
@click.option(
    "--duration",
    required=False,
    type=str,
    help="Duration (e.g., '31536000' '94608000')",
)
@click.option(
    "--product_description",
    required=True,
    type=str,
    help="Product description (e.g., 'redis oss' 'memcached' 'valkey')",
)
@click.option(
    "--offering_type",
    required=False,
    type=str,
    help=("Offering type " "(e.g., 'All Upfront', 'Partial Upfront', 'No Upfront')"),
)
@click.option(
    "--reserved_cache_nodes_offering_id",
    required=False,
    type=str,
    help="Reserved cache nodes offering ID (optional)",
)
@click.option(
    "--reserved_cache_node_id",
    required=False,
    type=str,
    help="Reserved cache node ID (optional)",
)
def elasticache(
    purchase_profile,
    region_name,
    quantity,
    reserved_cache_node_id,
    reserved_cache_nodes_offering_id,
    cache_node_type,
    duration,
    product_description,
    offering_type,
):
    """Retrieve ElastiCache offerings"""
    manager = ElastiCacheManager(region_name=region_name)
    """ 1. Get all offerings """
    offering_params = ElastiCacheParams(
        CacheNodeType=cache_node_type,
        Duration=duration,
        ProductDescription=product_description,
        OfferingType=offering_type,
        ReservedCacheNodesOfferingId=reserved_cache_nodes_offering_id,
    )
    offerings = manager.get_offerings(offering_params)

    """ 2. Add Purchase Command and Purchase Offering """
    purchase_params = ElastiCachePurchaseParams(
        purchase_profile=purchase_profile,
        region_name=region_name,
        quantity=quantity,
        reserved_cache_node_id=reserved_cache_node_id,
    )
    result = manager.add_keys_to_offerings(offerings, purchase_params)

    print(json.dumps(result, indent=2))
