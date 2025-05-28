# services/ai_service.py

class AIService:
    async def get_tese(self, tema: str, parametros: dict):
        # Simulação de geração de tese
        return {"tese": f"Tese gerada sobre {tema} com parâmetros {parametros}"}
