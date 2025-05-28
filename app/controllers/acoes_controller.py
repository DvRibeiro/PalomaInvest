# controllers/acoes_controller.py
from app.services.acoes_service import AcoesService

class AcoesController:
    def __init__(self):
        self.service = AcoesService()

    async def home(self):
        return await self.service.home()

    async def list_all_acoes_indicadores(self):
        return await self.service.list_all_acoes_indicadores()

    async def get_acao(self, ticker: int):
        return await self.service.get_acao(ticker)

    async def get_acao_detalhes(self, ticker: int):
        return await self.service.get_acao_detalhes(ticker)

    async def get_indicador_historico(self):
        return await self.service.get_indicador_historico()
