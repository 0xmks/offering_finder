import click
import json
from models.savingsplans_params import SavingsPlansParams
from managers.savingsplans_manager import SavingsPlansManager

# savingsplans subcommand
@click.command()
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
    """ Retrieve SavingsPlans offerings """
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