import subprocess

from flask.cli import FlaskGroup

from resthits.app.rest import create_app, db

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


if __name__ == "__main__":
    cli()
