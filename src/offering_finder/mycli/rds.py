import click
import json
from models.rds_params import RDSParams
from managers.rds_manager import RDSManager

# rds subcommand
@click.command()
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
    """ Retrieve Amazon RDS offerings """
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