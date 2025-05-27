from sqlalchemy.orm import Session
from sqlalchemy.orm import declarative_base
from config import engine
from models import Empresa, Indicador, FatoFinanceiro, Periodo, Setor, Base

try:
    # Criar todas as tabelas no banco de dados
    Base.metadata.create_all(bind=engine)
    print("Tabelas criadas com sucesso!")  
except Exception as e:
    print(f"Erro ao criar as tabelas: {e}") 
