# controllers/ai_controller.py
from fastapi import HTTPException
from app.services.ai_service import AI

class AIController:
    def __init__(self, session):
        self.session = session

    async def get_tese(self, ticker: str, dados: dict):
        try:
            ai = AI(ticker, self.session)
            return await ai.gerar_tese(dados)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Erro ao gerar tese: {str(e)}")
