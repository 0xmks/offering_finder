import click
from mycli.rds import rds
from mycli.elasticache import elasticache
from mycli.savingsplans import savingsplans
from mycli.opensearch import opensearch


@click.group()
def cli():
    pass

cli.add_command(rds)
cli.add_command(elasticache)
cli.add_command(savingsplans)
cli.add_command(opensearch)

if __name__ == "__main__":
    cli()
