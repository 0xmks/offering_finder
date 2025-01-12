import json
import click
from models.rds_params import RDSParams
from managers.rds_manager import RDSManager
from models.elasticache_params import ElastiCacheParams
from managers.elasticache_manager import ElastiCacheManager
from models.savingsplans_params import SavingsPlansParams
from managers.savingsplans_manager import SavingsPlansManager
from models.opensearch_params import OpenSearchParams, OpenSearchFilterParams, OpenSearchPurchaseParams
from managers.opensearch_manager import OpenSearchManager


@click.group(invoke_without_command=True)
@click.pass_context
def cli(ctx):
    if ctx.invoked_subcommand is None:
        click.echo("Please specify a subcommand.")
        ctx.exit()

# rds subcommand
@cli.command()
@click.option(
    "--product_description",
    required=True, 
    help="Product description (e.g., 'MySQL' 'PostgreSQL' 'aurora mysql' 'aurora postgresql')"
)
@click.option(
    "--db_instance_class",
    required=True,
    help="DB instance class (e.g., 'db.m5.large' 'db.r5.xlarge' 'db.t3.medium'...)"
)
@click.option(
    "--duration",
    required=True, 
    help="Duration (e.g., 31536000)"
)
@click.option(
    "--quantity",
    required=False,
    type=int,
    help="Quantity (e.g., 2)"
)
@click.option(
    "--region_name",
    required=True,
    help="AWS region name (e.g., 'ap-northeast-1')"
)
@click.option(
    "--multi_az", 
    is_flag=True, 
    help="Specify if the instance should be Multi-AZ"
)
@click.option(
    "--offering_type",
    required=True,
    help="Offering type (e.g., 'All Upfront', 'Partial Upfront', 'No Upfront')",
)
@click.option(
    "--reserved_instance_id",
    required=False,
    help="Reserved instance ID (optional)",
)
def rds(
    region_name,
    quantity,
    product_description,
    db_instance_class,
    duration,
    multi_az,
    offering_type,
    reserved_instance_id,
):
    params = RDSParams(
        product_description=product_description,
        db_instance_class=db_instance_class,
        duration=duration,
        quantity=quantity,
        multi_az=multi_az,
        offering_type=offering_type,
        reserved_instance_id=reserved_instance_id,
    )
    manager = RDSManager(region_name=region_name)
    offerings = manager.get_offering_ids(params)
    print(json.dumps(offerings, indent=2))

# elasticache subcommand
@cli.command()
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
    help="Cache node type (e.g., 'cache.m5.large' 'cache.r5.xlarge' 'cache.t3.medium'...)"
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
    help="Offering type (e.g., 'All Upfront', 'Partial Upfront', 'No Upfront')",
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

# savingsplans subcommand
@cli.command()
@click.option(
    "--region_name",
    default="ap-northeast-1",
    required=True,
    type=str,
    help="AWS region name (e.g., 'ap-northeast-1')"
)
@click.option(
    "--commitment",
    default=0.01,
    type=float,
    required=True,
    help="Commitment (e.g., 0.01)"
)
@click.option(
    "--durations",
    default=[31536000],
    multiple=True,
    type=int,
    help="Durations in seconds (e.g., 31536000 94608000)"
)
@click.option(
    "--plan_types",
    default=["Compute"],
    required=False,
    multiple=True,
    type=str,
    help="Plan type (e.g., 'Compute' 'EC2 Instance' 'EC2 Instance Family' 'Compute Instance' 'EC2 Instance Savings Plan')"
)
@click.option(
    "--offering_id",
    required=False,
    type=str,
    help="Offering ID"
)
@click.option(
    "--payment_options",
    default=["All Upfront"],
    required=False,
    multiple=True,
    type=str,
    help="Offering type (e.g., 'All Upfront', 'Partial Upfront', 'No Upfront')"
)
@click.option(
    "--client_token",
    required=False,
    type=str,
    help="Client token"
)
def savingsplans(
    region_name,
    commitment,
    durations,
    plan_types,
    offering_id,
    payment_options,
    client_token,
):
    params = SavingsPlansParams(
        region_name=region_name,
        commitment=commitment,
        offering_id=offering_id,
        durations=durations,
        plan_types=plan_types,
        payment_options=payment_options,
        client_token=client_token,
    )
    manager = SavingsPlansManager(region_name=region_name)
    offerings = manager.get_offering_ids(params)
    print(json.dumps(offerings, indent=2))

# Opensearch subcommand
@cli.command()
@click.option(
    "--region_name",
    required=True,
    type=str,
    help="AWS region name (e.g., 'ap-northeast-1') (required)"
)
@click.option(
    "--instance_type",
    required=False,
    type=str,
    help="Instance type (e.g., 'r5.large.search' 'm5.xlarge.search' 't3.medium.search'...) (optional)"
)
@click.option(
    "--duration",
    required=False,
    type=int,
    help="Duration (e.g., 31536000, 94608000) (optional)"
)
@click.option(
    "--payment_option",
    required=False,
    type=str,
    help="Offering type ('All_UPFRONT', 'PARTIAL_UPFRONT', 'NO_UPFRONT') (optional)"
)
@click.option(
    "--currency_code",
    required=False,
    type=str,
    help="Currency code ('USD' 'CNY') (optional)"
)
@click.option(
    "--reserved_instance_offering_id",
    required=False,
    type=str,
    help="ReservedInstanceOfferingId The ID of the Reserved Instance offering to purchase. (optional)"
)
@click.option(
    "--quantity",
    required=True,
    type=int,
    help="Quantity The number of OpenSearch instances to reserve. (e.g., 1) (optional)"
)
@click.option(
    "--reservation_name",
    required=False,
    type=str,
    help="Reservation name A customer-specified identifier to track this reservation. (e.g., 'my-reservation') (optional)"
)
def opensearch(
    region_name,
    reserved_instance_offering_id,
    instance_type,
    duration,
    currency_code,
    payment_option,
    quantity,
    reservation_name
):
    """ Retrieve all offerings """
    params_all = OpenSearchParams(
        reserved_instance_offering_id=reserved_instance_offering_id,
    )
    manager = OpenSearchManager(region_name=region_name)
    all_offerings = manager.get_offering_ids(params_all)

    """ Filter offerings to match the specified criteria """
    filter_params = OpenSearchFilterParams(
        reserved_instance_offering_id=reserved_instance_offering_id,
        instance_type=instance_type,
        duration=duration,
        currency_code=currency_code,
        payment_option=payment_option,
    )
    filterd_offerings = manager.filter_offerings(all_offerings, filter_params)

    """ Add Purchase Command and Purchase Offering """
    purchase_params = OpenSearchPurchaseParams(
        region_name=region_name,
        quantity=quantity,
        reservation_name=reservation_name,
    )
    result = manager.add_keys_to_offerings(filterd_offerings,purchase_params)
    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    cli()
