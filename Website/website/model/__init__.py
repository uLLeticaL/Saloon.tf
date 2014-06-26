"""The application's model objects"""
from website.model.meta import Session, Base


def init_model(engine):
    """Use Daemon's model instead of initializing a new one"""