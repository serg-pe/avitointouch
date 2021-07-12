from sqlalchemy import create_engine


DB_NAME = 'avitointouch.db'


def get_connection():
    engine = create_engine(f'sqlite:///{DB_NAME}')
    connection = engine.connect()
    return connection
