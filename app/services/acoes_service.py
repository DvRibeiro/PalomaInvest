# services/acoes_service.py

class AcoesService:
    async def home(self):
        return {"message": "Página inicial"}

    async def list_all_acoes_indicadores(self):
        return {"message": "Listando todas as ações com indicadores"}

    async def get_acao(self, ticker: int):
        return {"id": 1, "nome": "PETR4", "detalhes": None, "ticker": ticker}

    async def get_acao_detalhes(self, ticker: int):
        return {
            "id": 1,
            "nome": "PETR4",
            "detalhes": "Detalhes completos da ação PETR4",
            "indicadores": ["P/L", "ROE", "Dividend Yield"],
            "ticker": ticker
        }

    async def get_indicador_historico(self):
        return {
            "acao_id": 1,
            "historico": [10.5, 11.0, 10.8, 11.2]
        }
