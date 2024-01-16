import click
from .app import app, db

@app.cli.command()
def syncdb():
    """Create all missing tables"""
    db.create_all()