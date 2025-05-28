# controllers/ai_controller.py
from app.services.ai_service import AIService

class AIController:
    def __init__(self):
        self.service = AIService()

    async def get_tese(self, tema: str, parametros: dict):
        return await self.service.get_tese(tema, parametros)
