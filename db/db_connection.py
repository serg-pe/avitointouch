from os import getenv

from sqlalchemy import create_engine
from sqlalchemy.orm import Session


DB_NAME = getenv('DB_NAME')


def get_session() -> Session:
    engine = create_engine(f'sqlite:///{DB_NAME}')
    session = Session(engine)
    return session

