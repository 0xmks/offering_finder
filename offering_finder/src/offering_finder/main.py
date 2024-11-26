import json
import click
from clients.rds_client import RDSClient
from managers.rds_manager import OfferingRDSManager
from models.rds_params import OfferingParams


@click.command()
@click.option(
    "--product_description", required=True, help="Product description (e.g., MySQL)"
)
@click.option(
    "--db_instance_class", required=True, help="DB instance class (e.g., db.m5.large)"
)
@click.option("--duration", required=True, help="Duration (e.g., 31536000)")
@click.option("--quantity", required=True, type=int, help="Quantity (e.g., 2)")
@click.option(
    "--region_name", required=True, help="AWS region name (e.g., ap-northeast-1)"
)
@click.option(
    "--multi_az", is_flag=True, help="Specify if the instance should be Multi-AZ"
)
@click.option(
    "--offering_type",
    required=True,
    help="Offering type (e.g., All Upfront, Partial Upfront, No Upfront)",
)
@click.option(
    "--reserved_instance_id",
    required=False,
    help="Reserved instance ID (optional)",
)
def main(
    product_description,
    db_instance_class,
    duration,
    quantity,
    region_name,
    multi_az,
    offering_type,
    reserved_instance_id,
):
    params = OfferingParams(
        product_description=product_description,
        db_instance_class=db_instance_class,
        duration=duration,
        quantity=quantity,
        multi_az=multi_az,
        offering_type=offering_type,
        reserved_instance_id=reserved_instance_id,
    )

    manager = OfferingRDSManager(region_name=region_name)
    offerings = manager.get_offering_ids(params)
    print(json.dumps(offerings, indent=2))


if __name__ == "__main__":
    main()
