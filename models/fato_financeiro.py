from sqlalchemy import Column, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship
from models.base import Base

class FatoFinanceiro(Base):
    __tablename__ = 'fato_financeiro'

    id = Column(Integer, primary_key=True)
    valor = Column(Float, nullable=False)

    # Relacionamento com outras tabelas
    empresa_id = Column(Integer, ForeignKey('empresa.id'))
    empresa = relationship('Empresa', back_populates='fatos_financeiros')

    indicador_id = Column(Integer, ForeignKey('indicador.id'))
    indicador = relationship('Indicador', back_populates='fatos_financeiros')

    periodo_id = Column(Integer, ForeignKey('periodo.id'))
    periodo = relationship('Periodo')
