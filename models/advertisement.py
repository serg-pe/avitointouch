from sqlalchemy import Column, String, Integer, Numeric, DateTime
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class Advertisement(Base):
    """Advertisement data"""

    __tablename__ = 'advertisement'

    primary_id = Column('id', Integer, primary_key=True, autoincrement=True)
    title = Column('title', String(256), nullable=False)
    price = Column('price', Numeric(10, 2), nullable=False)
    specific_params = Column('specific_params', String(512), nullable=True)
    date = Column('date', DateTime, nullable=False)
    url = Column('url', String(128), nullable=False)

    def __str__(self) -> str:
        return f'{self.title}'