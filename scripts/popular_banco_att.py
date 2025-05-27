from sqlalchemy.orm import Session
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import fundamentus as fun
import pandas as pd
from config import engine
from models import Empresa, Setor, Indicador, Periodo, FatoFinanceiro, Base

# Configuração da conexão com o banco PostgreSQL
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
session = SessionLocal()

tickers = ['BBDC3', 'BBAS3', 'CMIG4', 'ISAE4', 'ITSA4', 'SAPR4',
           'CPFE3', 'FESA4', 'KLBN4', 'NEOE3', 'BLAU3', 'SLCE3']

def limpar_percentual(valor):
    try:
        if isinstance(valor, str):
            valor = valor.replace('%', '').replace(',', '.').strip()
        return float(valor)
    except Exception as e:
        raise ValueError(f"Erro ao converter '{valor}' para float.")

# Carrega os dados de múltiplos fundamentalistas
df_resultado = fun.get_resultado_raw()

for ticker in tickers:
    try:
        # ----------------- get_detalhes_papel ------------------
        detalhes = fun.get_detalhes_papel(ticker)
        row = detalhes.iloc[0]

        nome_empresa = row.get('Empresa')
        tipo = row.get('Tipo')
        setor_nome = row.get('Setor')

        # --- Setor
        setor = session.query(Setor).filter_by(nome=setor_nome).first()
        if not setor:
            setor = Setor(nome=setor_nome)
            session.add(setor)
            session.commit()

        # --- Empresa
        empresa = session.query(Empresa).filter_by(ticker=ticker).first()
        if not empresa:
            empresa = Empresa(
                nome=nome_empresa,
                tipo=tipo,
                ticker=ticker,
                setor_id=setor.id
            )
            session.add(empresa)
            session.commit()

        # --- Período
        data_str = row.get('Data_ult_cot')
        if isinstance(data_str, str):
            data = datetime.strptime(data_str, "%Y-%m-%d").date()
        else:
            data = datetime.now().date()

        periodo = session.query(Periodo).filter_by(data=data).first()
        if not periodo:
            periodo = Periodo(data=data)
            session.add(periodo)
            session.commit()

        # ----------------- get_resultado_raw ------------------
        if ticker in df_resultado.index:
            resultados = df_resultado.loc[ticker]
            for nome_indicador, valor in resultados.items():
                try:
                    nome = str(nome_indicador).strip()
                    valor_str = str(valor).replace('.', '').replace(',', '.')
                    valor_float = limpar_percentual(valor_str) if valor_str else None
                    if valor_float is None:
                        continue

                    indicador = session.query(Indicador).filter_by(nome=nome).first()
                    if not indicador:
                        indicador = Indicador(nome=nome)
                        session.add(indicador)
                        session.commit()

                    fato_existente = session.query(FatoFinanceiro).filter_by(
                        empresa_id=empresa.id,
                        indicador_id=indicador.id,
                        periodo_id=periodo.id
                    ).first()
                    if not fato_existente:
                        fato = FatoFinanceiro(
                            empresa_id=empresa.id,
                            indicador_id=indicador.id,
                            periodo_id=periodo.id,
                            valor=valor_float
                        )
                        session.add(fato)
                except Exception as e:
                    print(f"[!] Erro em múltiplo '{nome_indicador}' para {ticker}: {e}")

        # ----------------- dados extras de detalhes.py ------------------
        colunas_para_importar = [
            'Min_52_sem', 'Max_52_sem', 'Vol_med_2m', 'Valor_de_mercado', 'Valor_da_firma',
            'Nro_Acoes', 'PL', 'PVP', 'PEBIT', 'PSR', 'PAtivos', 'PCap_Giro',
            'PAtiv_Circ_Liq', 'Div_Yield', 'EV_EBITDA', 'EV_EBIT', 'Cres_Rec_5a',
            'LPA', 'VPA', 'Marg_Bruta', 'Marg_EBIT', 'Marg_Liquida', 'EBIT_Ativo',
            'ROIC', 'ROE', 'Liquidez_Corr', 'Div_Br_Patrim', 'Giro_Ativos',
            'Ativo', 'Cart_de_Credito', 'Depositos', 'Patrim_Liq',
            'Result_Int_Financ_12m', 'Rec_Servicos_12m', 'Lucro_Liquido_12m',
            'Result_Int_Financ_3m', 'Rec_Servicos_3m', 'Lucro_Liquido_3m'
        ]

        for coluna in colunas_para_importar:
            try:
                valor = row.get(coluna, None)
                if valor in [None, '', '-']:
                    continue
                valor_str = str(valor).replace('.', '').replace(',', '.')
                valor_float = limpar_percentual(valor_str)

                indicador = session.query(Indicador).filter_by(nome=coluna).first()
                if not indicador:
                    indicador = Indicador(nome=coluna)
                    session.add(indicador)
                    session.commit()

                fato_existente = session.query(FatoFinanceiro).filter_by(
                    empresa_id=empresa.id,
                    indicador_id=indicador.id,
                    periodo_id=periodo.id
                ).first()
                if not fato_existente:
                    fato = FatoFinanceiro(
                        empresa_id=empresa.id,
                        indicador_id=indicador.id,
                        periodo_id=periodo.id,
                        valor=valor_float
                    )
                    session.add(fato)
            except Exception as e:
                print(f"[!] Erro ao processar '{coluna}' para {ticker}: {e}")

        session.commit()
        print(f"[✓] {ticker} importado com sucesso.")

    except Exception as e:
        print(f"[X] Falha ao importar {ticker}: {e}")
        continue

session.close()
