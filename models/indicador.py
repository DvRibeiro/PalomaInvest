from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from models.base import Base

class Indicador(Base):
    __tablename__ = 'indicador'

    id = Column(Integer, primary_key=True)
    nome = Column(String, nullable=False, unique=True)

    # Relacionamento com fato_financeiro
    fatos_financeiros = relationship('FatoFinanceiro', back_populates='indicador')
