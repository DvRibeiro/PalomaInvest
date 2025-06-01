# controllers/acoes_controller.py
from fastapi import HTTPException
from app.services.acoes_service import AcoesService

class AcoesController:
    def __init__(self, session):
        self.service = AcoesService(session)

    async def home(self):
        return await self.service.home()

    async def list_all_acoes_indicadores(self):
        return await self.service.list_all_acoes_indicadores()

    async def get_acao(self, ticker: str):
        if not ticker or len(ticker.strip()) == 0:
            raise HTTPException(status_code=400, detail="Ticker não informado")
        
        return await self.service.get_acao(ticker)

    async def get_acao_detalhes(self, ticker: str):        
        if not ticker or len(ticker.strip()) == 0:
            raise HTTPException(status_code=400, detail="Ticker não informado")
        
        return await self.service.get_acao_detalhes(ticker)

    async def get_indicador_historico(self):
        return await self.service.get_indicador_historico()
