from sqlalchemy import Column, Integer, Date
from models.base import Base

class Periodo(Base):
    __tablename__ = 'periodo'

    id = Column(Integer, primary_key=True)
    data = Column(Date, nullable=False)
