"""The application's model objects"""
from website.model.meta import Session, Base


def init_model(engine):
    """Overwrite Pylon's SQLAlchemy session with Daemon's one"""