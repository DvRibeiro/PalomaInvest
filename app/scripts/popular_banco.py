import fundamentus as fun
from sqlalchemy.orm import Session
from datetime import datetime

from app.config.config import engine
from models import Empresa, Setor, Indicador, Periodo, FatoFinanceiro

from sqlalchemy.orm import sessionmaker

# Cria sessão
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
db: Session = SessionLocal()

# Recupera dados
df_multiples = fun.get_resultado_raw()
tickers = df_multiples.index.tolist()

def get_or_create_setor(nome_setor):
    setor = db.query(Setor).filter_by(nome=nome_setor).first()
    if not setor:
        setor = Setor(nome=nome_setor)
        db.add(setor)
        db.commit()
        db.refresh(setor)
    return setor

def criar_periodo_atual():
    hoje = datetime.today()
    periodo = db.query(Periodo).filter_by(ano=hoje.year, trimestre=((hoje.month - 1) // 3 + 1)).first()
    if not periodo:
        periodo = Periodo(ano=hoje.year, trimestre=((hoje.month - 1) // 3 + 1))
        db.add(periodo)
        db.commit()
        db.refresh(periodo)
    return periodo

periodo = criar_periodo_atual()

for ticker in tickers:
    try:
        detalhes = fun.get_detalhes_papel(ticker)
        linha = detalhes.iloc[0]

        # SETOR
        setor = get_or_create_setor(linha['Setor'])

        # EMPRESA
        empresa = db.query(Empresa).filter_by(ticker=ticker).first()
        if not empresa:
            empresa = Empresa(
                ticker=ticker,
                nome=linha['Empresa'],
                tipo=linha['Tipo'],
                setor_id=setor.id
            )
            db.add(empresa)
            db.commit()
            db.refresh(empresa)

        # INDICADOR
        indicador = Indicador(
            empresa_id=empresa.id,
            cotacao=linha['Cotacao'],
            data_atualizacao=datetime.strptime(linha['Data_ult_cot'], "%d/%m/%Y")
        )
        db.add(indicador)
        db.commit()
        db.refresh(indicador)

        # FATO FINANCEIRO (exemplo com alguns campos)
        fato = FatoFinanceiro(
            indicador_id=indicador.id,
            periodo_id=periodo.id,
            lpa=linha.get('LPA') or 0.0,
            vpa=linha.get('VPA') or 0.0,
            roe=linha.get('ROE') or 0.0,
            margem_liquida=linha.get('Marg_Liquida') or 0.0,
            patrimonio_liquido=linha.get('Patrim_Liq') or 0.0,
            div_yield=linha.get('Div_Yield') or 0.0
        )
        db.add(fato)
        db.commit()

        print(f"[OK] Dados inseridos para {ticker}")

    except Exception as e:
        print(f"[ERRO] {ticker}: {e}")
        db.rollback()

db.close()
