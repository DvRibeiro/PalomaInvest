from collections import defaultdict
from sqlalchemy import Integer, func, join, literal_column, select
from models import Empresa, Indicador, FatoFinanceiro, Periodo, Setor, Base
from fastapi import HTTPException, status
from sqlalchemy.exc import SQLAlchemyError


class AcoesService:
    def __init__(self, session):
        self.session = session

    async def home(self):
        return {"message": "Página inicial"}

    async def list_all_acoes_indicadores(self):
        try:
            joinClause = join(
                FatoFinanceiro, Empresa, FatoFinanceiro.empresa_id == Empresa.id
            ).join(
                Setor, Empresa.setor_id == Setor.id
            ).join(
                Indicador, FatoFinanceiro.indicador_id == Indicador.id
            ).join(
                Periodo, FatoFinanceiro.periodo_id == Periodo.id
            )

            stmt = select(
                Empresa.ticker.label("codigo_acao"),
                Empresa.nome.label("nome_empresa"),
                Setor.nome.label("setor"),
                Indicador.nome.label("indicador"),
                FatoFinanceiro.valor.label("valor"),
                func.extract("year", Periodo.data).label("ano"),
                func.ceil(func.extract("month", Periodo.data) / 3.0).cast(Integer).label("trimestre")
            ).select_from(joinClause).order_by(
                Empresa.ticker,
                literal_column("ano").desc(),
                literal_column("trimestre").desc(),
                Indicador.nome
            )

            result = await self.session.execute(stmt)
            rows = result.fetchall()

            if not rows:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Nenhuma ação encontrada.")

            acoes_dict = defaultdict(lambda: {
                "codigo_acao": "",
                "nome_empresa": "",
                "setor": "",
                "periodo": {},
                "indicadores": []
            })

            for row in rows:
                codigo = row.codigo_acao
                acoes_dict[codigo]["codigo_acao"] = row.codigo_acao
                acoes_dict[codigo]["nome_empresa"] = row.nome_empresa
                acoes_dict[codigo]["setor"] = row.setor
                acoes_dict[codigo]["periodo"] = {
                    "ano": row.ano,
                    "trimestre": row.trimestre
                }
                acoes_dict[codigo]["indicadores"].append({
                    "nome": row.indicador,
                    "valor": float(row.valor)
                })

            return list(acoes_dict.values())

        except SQLAlchemyError as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Erro ao buscar ações no banco de dados.")

    async def get_acao(self, ticker: str):
        return {"message": "Coming Soon..."}

    async def get_acao_detalhes(self, ticker: str):
        if not ticker or not ticker.strip():
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Ticker não informado.")

        try:
            joinClause = join(
                FatoFinanceiro, Empresa, FatoFinanceiro.empresa_id == Empresa.id
            ).join(
                Setor, Empresa.setor_id == Setor.id
            ).join(
                Indicador, FatoFinanceiro.indicador_id == Indicador.id
            ).join(
                Periodo, FatoFinanceiro.periodo_id == Periodo.id
            )

            stmt = select(
                Empresa.ticker.label("codigo_acao"),
                Empresa.nome.label("nome_empresa"),
                Setor.nome.label("setor"),
                Indicador.nome.label("indicador"),
                FatoFinanceiro.valor.label("valor"),
                func.extract("year", Periodo.data).label("ano"),
                func.ceil(func.extract("month", Periodo.data) / 3.0).cast(Integer).label("trimestre")
            ).select_from(joinClause).filter(
                Empresa.ticker == ticker.upper()
            ).order_by(
                Empresa.ticker,
                literal_column("ano").desc(),
                literal_column("trimestre").desc(),
                Indicador.nome
            )

            result = await self.session.execute(stmt)
            rows = result.fetchall()

            if not rows:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Ação com ticker '{ticker}' não encontrada.")

            # Inicializa o objeto resultado
            acao = {
                "codigo_acao": rows[0].codigo_acao,
                "nome_empresa": rows[0].nome_empresa,
                "setor": rows[0].setor,
                "periodo": {
                    "ano": int(rows[0].ano),
                    "trimestre": int(rows[0].trimestre)
                },
                "indicadores": []
            }

            # Preenche os indicadores
            for row in rows:
                acao["indicadores"].append({
                    "nome": row.indicador,
                    "valor": float(row.valor)
                })

            return acao

        except SQLAlchemyError:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Erro ao buscar detalhes da ação.")

    async def get_indicador_historico(self):
        return {
            "acao_id": 1,
            "historico": [10.5, 11.0, 10.8, 11.2]
        }
