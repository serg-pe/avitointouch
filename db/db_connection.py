from os import getenv

from sqlalchemy import create_engine


DB_NAME = getenv('DB_NAME')


def get_connection():
    engine = create_engine(f'sqlite:///{DB_NAME}')
    connection = engine.connect()
    return connection
