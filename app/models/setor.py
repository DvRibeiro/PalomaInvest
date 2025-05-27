from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from models.base import Base

class Setor(Base):
    __tablename__ = 'setor'

    id = Column(Integer, primary_key=True)
    nome = Column(String, nullable=False, unique=True)

    # Relacionamento com empresas
    empresas = relationship('Empresa', back_populates='setor')
