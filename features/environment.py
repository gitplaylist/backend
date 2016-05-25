"""Define context before any tests run."""
from app import create_app


def before_all(context):
    """Create the context bag."""
    context.app = create_app()


def after_all(context):
    """Destroy the context bag."""
