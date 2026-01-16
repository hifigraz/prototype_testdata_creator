from sqlalchemy import create_engine as sqlalchemy_create_engine

from ..model import Base


def create_engine(connection_string: str):
    engine = sqlalchemy_create_engine(connection_string)
    Base.metadata.create_all(engine)
    return engine
