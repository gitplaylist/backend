"""Define context before any tests run."""
import os


def before_all(context):
    """Create the context bag."""
    # Change the configuration on the fly
    os.environ['ENV'] = 'testing'

    # Import this now because the environment variable
    # should be changed before this happens.
    from app import create_app, db
    context.app = create_app()

    # Create all the tables in memory.
    with context.app.app_context():
        db.create_all()

    # Create the test client.
    context.client = context.app.test_client()


def after_all(context):
    """Destroy the context bag."""
