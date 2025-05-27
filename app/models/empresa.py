from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from models.base import Base

class Empresa(Base):
    __tablename__ = 'empresa'

    id = Column(Integer, primary_key=True)
    nome = Column(String, nullable=False)
    ticker = Column(String, nullable=False, unique=True)
    tipo = Column(String, nullable=True)

    # Relacionamento com outras tabelas
    setor_id = Column(Integer, ForeignKey('setor.id'))
    setor = relationship('Setor', back_populates='empresas')

    # Relacionamento com fato_financeiro
    fatos_financeiros = relationship('FatoFinanceiro', back_populates='empresa')
