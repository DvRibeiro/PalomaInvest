from fastapi import APIRouter, Request
from app.controllers.ai_controller import AIController

ai = AIController()
router = APIRouter(prefix="/api")

@router.post("/gerarTese")
async def gerar_tese(request: Request):
    data = await request.json()
    return await ai.get_tese(data)
