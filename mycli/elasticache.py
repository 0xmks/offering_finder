import click
import json
from src.offering_finder.models.elasticache_params import ElastiCacheParams
from src.offering_finder.managers.elasticache_manager import ElastiCacheManager


# elasticache subcommand
@click.command()
@click.option(
    "--region_name",
    required=True,
    help="AWS region name (e.g., 'ap-northeast-1')"
)
@click.option(
    "--quantity",
    required=True,
    type=int,
    help="Quantity (e.g., 1)"
)
@click.option(
    "--cache_node_type",
    required=True,
    help=(
        "Cache node type "
        "(e.g., 'cache.m5.large' 'cache.r5.xlarge' 'cache.t3.medium'...)"
    )
)
@click.option(
    "--duration",
    required=False,
    help="Duration (e.g., 31536000 94608000)"
)
@click.option(
    "--product_description",
    required=True,
    help="Product description (e.g., 'redis oss' 'memcached' 'valkey')",
)
@click.option(
    "--offering_type",
    required=False,
    help=(
        "Offering type "
        "(e.g., 'All Upfront', 'Partial Upfront', 'No Upfront')"
    )
)
@click.option(
    "--reserved_cache_nodes_offering_id",
    required=False,
    help="Reserved cache nodes offering ID (optional)",
)
@click.option(
    "--reserved_cache_node_id",
    required=False,
    help="Reserved cache node ID (optional)",
)
def elasticache(
    region_name,
    quantity,
    reserved_cache_nodes_offering_id,
    cache_node_type,
    duration,
    product_description,
    offering_type,
    reserved_cache_node_id,
):
    """ Retrieve ElastiCache offerings """
    params = ElastiCacheParams(
        region_name=region_name,
        quantity=quantity,
        reserved_cache_nodes_offering_id=reserved_cache_nodes_offering_id,
        cache_node_type=cache_node_type,
        duration=duration,
        product_description=product_description,
        offering_type=offering_type,
        reserved_cache_node_id=reserved_cache_node_id,
    )
    manager = ElastiCacheManager(region_name=region_name)
    offerings = manager.get_offering_ids(params)
    print(json.dumps(offerings, indent=2))
