import click
import json
from src.offering_finder.models.savingsplans_params import (
    SavingsPlansParams,
    SavingsPlansPurchaseParams,
)
from src.offering_finder.managers.savingsplans_manager import SavingsPlansManager


# savingsplans subcommand
@click.command()
@click.option(
    "--purchase_profile",
    required=False,
    type=str,
    help="Purchase command set a named profile (e.g., 'default' 'my-profile')",
)
@click.option(
    "--region_name",
    default="ap-northeast-1",
    required=True,
    type=str,
    help="AWS region name (e.g., 'ap-northeast-1')",
)
@click.option(
    "--offering_id",
    required=False,
    multiple=True,
    type=str,
    help="The IDs of the offerings.",
)
@click.option(
    "--payment_options",
    default=["All Upfront"],
    required=False,
    multiple=True,
    type=str,
    help="Offering type (e.g., 'All Upfront', 'Partial Upfront', 'No Upfront')",
)
@click.option(
    "--product_type",
    required=False,
    type=str,
    help="Offering type ('EC2'|'Fargate'|'Lambda'|'SageMaker')",
)
@click.option(
    "--plan_types",
    default=["Compute"],
    required=False,
    multiple=True,
    type=str,
    help="Plan type ('Compute'|'EC2Instance'|'SageMaker')",
)
@click.option(
    "--commitment",
    default=0.01,
    type=float,
    required=True,
    help="Commitment (e.g., 0.01)",
)
@click.option(
    "--currency",
    type=str,
    required=False,
    help="currency ('CNY'|'USD')",
)
@click.option(
    "--durations",
    default=[31536000],
    multiple=True,
    required=True,
    type=int,
    help="Durations in seconds ( 31536000 | 94608000 )",
)
@click.option(
    "--purchase_time",
    required=False,
    type=str,
    help="The purchase time of the Savings Plan in UTC format (YYYY-MM-DDTHH:MM:SSZ).",
)
@click.option("--client_token", required=False, type=str, help="Client token")
def savingsplans(
    purchase_profile,
    region_name,
    commitment,
    durations,
    plan_types,
    product_type,
    offering_id,
    payment_options,
    client_token,
    currency,
    purchase_time,
):
    """Retrieve SavingsPlans offerings"""
    manager = SavingsPlansManager(region_name=region_name)
    """ 1. Get all offerings """
    params = SavingsPlansParams(
        offeringIds=offering_id,
        paymentOptions=payment_options,
        durations=durations,
        planTypes=plan_types,
        productType=product_type,
        currencies=currency,
    )
    offerings = manager.get_offerings(params)

    """ 2. Add Purchase Command and Purchase Offering """
    purchase_params = SavingsPlansPurchaseParams(
        purchase_profile=purchase_profile,
        region_name=region_name,
        commitment=float(commitment),
        client_token=client_token,
        purchase_time=purchase_time,
    )
    result = manager.add_keys_to_offerings(offerings, purchase_params)

    print(json.dumps(result, indent=2))
