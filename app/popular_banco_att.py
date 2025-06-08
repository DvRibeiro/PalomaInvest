import asyncio
from datetime import datetime
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from config.DBconfig import AsyncSessionLocal
from models import Empresa, Setor, Indicador, Periodo, FatoFinanceiro
import fundamentus as fun


tickers = ['BBDC3', 'BBAS3', 'CMIG4', 'ISAE4', 'ITSA4', 'SAPR4',
           'CPFE3', 'FESA4', 'KLBN4', 'NEOE3', 'BLAU3', 'SLCE3']

def limpar_percentual(valor):
    try:
        if isinstance(valor, str):
            valor = valor.replace('%', '').replace(',', '.').strip()
        return float(valor)
    except Exception as e:
        raise ValueError(f"Erro ao converter '{valor}' para float.")


async def importar_dados():

    async with AsyncSessionLocal() as session:
        for ticker in tickers:
            try:
                detalhes = fun.get_detalhes_papel(ticker)
                row = detalhes.iloc[0]

                nome_empresa = row.get('Empresa')
                tipo = row.get('Tipo')
                setor_nome = row.get('Setor')

                # Setor
                result = await session.execute(select(Setor).filter_by(nome=setor_nome))
                setor = result.scalar_one_or_none()
                if not setor:
                    setor = Setor(nome=setor_nome)
                    session.add(setor)
                    await session.commit()
                    await session.refresh(setor)

                # Empresa
                result = await session.execute(select(Empresa).filter_by(ticker=ticker))
                empresa = result.scalar_one_or_none()
                if not empresa:
                    empresa = Empresa(
                        nome=nome_empresa,
                        tipo=tipo,
                        ticker=ticker,
                        setor_id=setor.id
                    )
                    session.add(empresa)
                    await session.commit()
                    await session.refresh(empresa)

                # Período
                data_str = row.get('Data_ult_cot')
                data = datetime.strptime(data_str, "%Y-%m-%d").date() if isinstance(data_str, str) else datetime.now().date()

                result = await session.execute(select(Periodo).filter_by(data=data))
                periodo = result.scalar_one_or_none()
                if not periodo:
                    periodo = Periodo(data=data)
                    session.add(periodo)
                    await session.commit()
                    await session.refresh(periodo)

                colunas_para_importar = ['Cotacao','Data_ult_cot', 'Min_52_sem', 'Max_52_sem', 'Vol_med_2m',
                    'Valor_de_mercado', 'Valor_da_firma', 'Ult_balanco_processado',
                    'Nro_Acoes', 'PL', 'PVP', 'PEBIT', 'PSR', 'PAtivos', 'PCap_Giro',
                    'PAtiv_Circ_Liq', 'Div_Yield', 'EV_EBITDA', 'EV_EBIT', 'Cres_Rec_5a',
                    'LPA', 'VPA', 'Marg_Bruta', 'Marg_EBIT', 'Marg_Liquida', 'EBIT_Ativo',
                    'ROIC', 'ROE', 'Liquidez_Corr', 'Div_Br_Patrim', 'Giro_Ativos', 'Ativo',
                    'Cart_de_Credito', 'Depositos', 'Patrim_Liq', 'Result_Int_Financ_12m',
                    'Rec_Servicos_12m', 'Lucro_Liquido_12m', 'Result_Int_Financ_3m',
                    'Rec_Servicos_3m', 'Lucro_Liquido_3m']
                
                indicadores_decimais = ['PL', 'PVP', 'LPA', 'VPA', 'PSR', 'PEBIT', 'EV_EBITDA', 'EV_EBIT', 'Giro_Ativos','Liquidez_Corr',
                    'Div_Br_Patrim', 'PAtiv_Circ_Liq', 'PAtivos', 'PCap_Giro']
                
                for coluna in colunas_para_importar:
                    try:
                        valor = row.get(coluna, None)
                        if valor in [None, '', '-']:
                            continue
                        valor_str = str(valor).replace('.', '').replace(',', '.')
                        
                        if coluna in indicadores_decimais:
                            valor = (float(valor) / 100)

                        valor_float = limpar_percentual(valor)

                        result = await session.execute(select(Indicador).filter_by(nome=coluna))
                        indicador = result.scalar_one_or_none()
                        if not indicador:
                            indicador = Indicador(nome=coluna)
                            session.add(indicador)
                            await session.commit()
                            await session.refresh(indicador)

                        result = await session.execute(
                            select(FatoFinanceiro).filter_by(
                                empresa_id=empresa.id,
                                indicador_id=indicador.id,
                                periodo_id=periodo.id
                            )
                        )
                        fato_existente = result.scalar_one_or_none()
                        if not fato_existente:
                            fato = FatoFinanceiro(
                                empresa_id=empresa.id,
                                indicador_id=indicador.id,
                                periodo_id=periodo.id,
                                valor=valor_float
                            )
                            session.add(fato)
                    except Exception as e:
                        print(f">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>[!] Erro ao processar '{coluna}' para {ticker}: {e}")

                await session.commit()
                print(f"[✓] {ticker} importado com sucesso.")

            except Exception as e:
                print(f"[X] Falha ao importar {ticker}: {e}")
                continue


if __name__ == "__main__":
    asyncio.run(importar_dados())