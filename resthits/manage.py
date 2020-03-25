import subprocess

import click
from flask.cli import FlaskGroup

from resthits.app.rest import create_app, db
from resthits.domain.utils import SampleDataFactory

app = create_app()
cli = FlaskGroup(create_app=create_app)


@cli.command()
def create_db():
    db.drop_all()
    db.create_all()
    db.session.commit()


@cli.command()
def drop_db():
    """Drops the db tables."""
    db.drop_all()


@cli.command()
def test_pytest_with_plugins():
    """Runs pytest with plugins on the gatekeeper."""
    subprocess.run(["pytest", "--ignore=migrations", "--black", "--isort", "--flakes"])


@cli.command()
def test_pytest():
    """Runs pytest on the gatekeeper."""
    subprocess.run(["pytest"])


@cli.command()
@click.argument("hits_number", type=int)
def create_sample_data(hits_number):
    """Create sample data in db"""
    factory = SampleDataFactory(database=db)
    factory.add_sample_hits_to_db(hits_number)
    print("Sample data created.")


if __name__ == "__main__":
    cli()
