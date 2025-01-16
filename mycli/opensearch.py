import click
import json
from src.offering_finder.models.opensearch_params import (
    OpenSearchParams,
    OpenSearchFilterParams,
    OpenSearchPurchaseParams,
)
from src.offering_finder.managers.opensearch_manager import OpenSearchManager


# Opensearch subcommand
@click.command()
@click.option(
    "--purchase_profile",
    required=False,
    type=str,
    help="Purchase command set a named profile (e.g., 'default' 'my-profile')",
)
@click.option(
    "--region_name",
    required=True,
    type=str,
    help="AWS region name (e.g., 'ap-northeast-1') (required)",
)
@click.option(
    "--instance_type",
    required=False,
    type=str,
    help=(
        "Instance type "
        "(e.g., 'r5.large.search' 'm5.xlarge.search' 't3.medium.search'...)"
    ),
)
@click.option(
    "--duration",
    required=False,
    type=int,
    help=("The duration, in seconds. (e.g., 31536000, 94608000)"),
)
@click.option(
    "--payment_option",
    required=False,
    type=str,
    help=("Offering type ('All_UPFRONT', 'PARTIAL_UPFRONT', 'NO_UPFRONT')"),
)
@click.option(
    "--currency_code", required=False, type=str, help=("Currency code ('USD' 'CNY')")
)
@click.option(
    "--reserved_instance_offering_id",
    required=False,
    type=str,
    help=(
        "ReservedInstanceOfferingId The ID of the Reserved Instance offering to purchase."
    ),
)
@click.option(
    "--quantity",
    required=True,
    type=int,
    help=("Quantity The number of OpenSearch instances to reserve. (e.g., 1)"),
)
@click.option(
    "--reservation_name",
    required=False,
    type=str,
    help=(
        "Reservation name A customer-specified identifier to track this reservation. "
        "(e.g., 'my-reservation') (optional)"
    ),
)
def opensearch(
    purchase_profile,
    region_name,
    reserved_instance_offering_id,
    instance_type,
    duration,
    currency_code,
    payment_option,
    quantity,
    reservation_name,
):
    """Retrieve OpenSearch offerings"""
    """ 1. Get all offerings """
    params_all = OpenSearchParams(
        ReservedInstanceOfferingId=reserved_instance_offering_id,
    )
    manager = OpenSearchManager(region_name=region_name)
    all_offerings = manager.get_offering_ids(params_all)

    """ 2. Filter offerings to match the specified criteria """
    filter_params = OpenSearchFilterParams(
        ReservedInstanceOfferingId=reserved_instance_offering_id,
        InstanceType=instance_type,
        Duration=duration,
        CurrencyCode=currency_code,
        PaymentOption=payment_option,
    )
    filter_offerings = manager.filter_offerings(all_offerings, filter_params)

    """ 3. Add Purchase Command and Purchase Offering """
    purchase_params = OpenSearchPurchaseParams(
        purchase_profile=purchase_profile,
        region_name=region_name,
        quantity=quantity,
        reservation_name=reservation_name,
    )
    result = manager.add_keys_to_offerings(filter_offerings, purchase_params)
    print(json.dumps(result, indent=2))
