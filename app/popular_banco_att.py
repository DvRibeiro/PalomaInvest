import asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import fundamentus as fun
from config.DBconfig import engine  # engine criado com create_async_engine
from models import Empresa, Setor, Indicador, Periodo, FatoFinanceiro


# Criar AsyncSession
AsyncSessionLocal = sessionmaker(
    bind=engine,
    expire_on_commit=False,
    class_=AsyncSession
)

tickers = ['BBDC3', 'BBAS3', 'CMIG4', 'ISAE4', 'ITSA4', 'SAPR4',
           'CPFE3', 'FESA4', 'KLBN4', 'NEOE3', 'BLAU3', 'SLCE3']

def normalizar_valor(indicador, valor):
    if valor in ['-', None, '']:
        return None

    indicadores_div100 = ['PL', 'PVP', 'VPA', 'LPA', 'PSR', 'PEBIT', 'PCap_Giro', 'PAtivos', 'PAtiv_Circ_Liq']

    try:
        if indicador in indicadores_div100:
            return float(valor) / 100

        return float(valor)
    except Exception as e:
        raise ValueError(f"Erro ao converter '{valor}' para float.")

def limpar_percentual(valor):
    try:
        if isinstance(valor, str):
            valor = valor.replace('%', '').replace(',', '.').strip()
        return float(valor)
    except Exception as e:
        raise ValueError(f"Erro ao converter '{valor}' para float.")


async def main():
    async with AsyncSessionLocal() as session:
        for ticker in tickers:
            try:
                # detalhes é DataFrame síncrono
                detalhes = fun.get_detalhes_papel(ticker)
                row = detalhes.iloc[0]

                nome_empresa = row.get('Empresa')
                tipo = row.get('Tipo')
                setor_nome = row.get('Setor')

                # --- Setor
                result = await session.execute(select(Setor).filter_by(nome=setor_nome))
                setor = result.scalars().first()
                if not setor:
                    setor = Setor(nome=setor_nome)
                    session.add(setor)
                    await session.commit()

                # --- Empresa
                result = await session.execute(select(Empresa).filter_by(ticker=ticker))
                empresa = result.scalars().first()
                if not empresa:
                    empresa = Empresa(
                        nome=nome_empresa,
                        tipo=tipo,
                        ticker=ticker,
                        setor_id=setor.id
                    )
                    session.add(empresa)
                    await session.commit()

                # --- Período
                data_str = row.get('Data_ult_cot')
                if isinstance(data_str, str):
                    data = datetime.strptime(data_str, "%Y-%m-%d").date()
                else:
                    data = datetime.now().date()

                result = await session.execute(select(Periodo).filter_by(data=data))
                periodo = result.scalars().first()
                if not periodo:
                    periodo = Periodo(data=data)
                    session.add(periodo)
                    await session.commit()

                # Processar indicadores
                for nome_indicador, valor in row.items():
                    try:
                        if valor in [None, '', '-']:
                            continue

                        valor_str = str(valor).replace('.', '').replace(',', '.')
                        valor_float = limpar_percentual(valor_str)
                        valor_float = normalizar_valor(nome_indicador, valor_float)

                        result = await session.execute(select(Indicador).filter_by(nome=nome_indicador))
                        indicador = result.scalars().first()
                        if not indicador:
                            indicador = Indicador(nome=nome_indicador)
                            session.add(indicador)
                            await session.commit()

                        result = await session.execute(
                            select(FatoFinanceiro).filter_by(
                                empresa_id=empresa.id,
                                indicador_id=indicador.id,
                                periodo_id=periodo.id
                            )
                        )
                        fato_existente = result.scalars().first()
                        if not fato_existente:
                            fato = FatoFinanceiro(
                                empresa_id=empresa.id,
                                indicador_id=indicador.id,
                                periodo_id=periodo.id,
                                valor=valor_float
                            )
                            session.add(fato)

                    except Exception as e:
                        print(f"[!] Erro ao processar '{nome_indicador}' para {ticker}: {e}")

                await session.commit()
                print(f"[✓] {ticker} importado com sucesso.")

            except Exception as e:
                print(f"[X] Falha ao importar {ticker}: {e}")
                continue

asyncio.run(main())
