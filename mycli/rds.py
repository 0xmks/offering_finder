import click
import json
from src.offering_finder.models.rds_params import RDSParams, RDSPurchaseParams
from src.offering_finder.managers.rds_manager import RDSManager


# rds subcommand
@click.command()
@click.option(
    "--purchase_profile",
    required=False,
    type=str,
    help="Purchase command set a named profile (e.g., 'default' 'my-profile')",
)
@click.option(
    "--reserved_instance_offering_id",
    required=False,
    type=str,
    help="Reserved instance offering ID",
)
@click.option(
    "--product_description",
    required=True,
    type=str,
    help="Product description (e.g., 'MySQL' 'PostgreSQL' 'aurora mysql' 'aurora postgresql')",
)
@click.option(
    "--db_instance_class",
    required=True,
    type=str,
    help="DB instance class (e.g., 'db.m5.large' 'db.r5.xlarge' 'db.t3.medium'...)",
)
@click.option(
    "--duration", required=True, type=str, help="Duration (e.g., '31536000' '94608000')"
)
@click.option("--quantity", required=True, type=int, help="Quantity (e.g., 2)")
@click.option(
    "--region_name",
    required=True,
    type=str,
    help="AWS region name (e.g., 'ap-northeast-1')",
)
@click.option(
    "--multi_az", is_flag=True, help="Specify if the instance should be Multi-AZ"
)
@click.option(
    "--offering_type",
    required=True,
    type=str,
    help="Offering type (e.g., 'All Upfront', 'Partial Upfront', 'No Upfront')",
)
@click.option(
    "--reserved_instance_id",
    required=False,
    type=str,
    help="Reserved instance ID (optional)",
)
def rds(
    purchase_profile,
    region_name,
    reserved_instance_offering_id,
    quantity,
    product_description,
    db_instance_class,
    duration,
    multi_az,
    offering_type,
    reserved_instance_id,
):
    """Retrieve Amazon RDS offerings"""
    manager = RDSManager(region_name=region_name)
    """ 1. Get all offerings """
    params = RDSParams(
        ReservedDBInstanceOfferingId=reserved_instance_offering_id,
        ProductDescription=product_description,
        DBInstanceClass=db_instance_class,
        Duration=duration,
        MultiAZ=multi_az,
        OfferingType=offering_type,
    )
    offerings = manager.get_offerings(params)

    """ 2. Add Purchase Command and Purchase Offering """
    purchase_params = RDSPurchaseParams(
        purchase_profile=purchase_profile,
        region_name=region_name,
        quantity=quantity,
        reserved_instance_id=reserved_instance_id,
    )
    result = manager.add_keys_to_offerings(offerings, purchase_params)

    print(json.dumps(result, indent=2))
