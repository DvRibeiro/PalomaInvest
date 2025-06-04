from fastapi import APIRouter, Request, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.controllers.ai_controller import AIController
from app.config.DBconfig import get_session
from pydantic import BaseModel

router = APIRouter(prefix="/api")

class DadosEntrada(BaseModel):
    lpa: float
    vpa: float

@router.post("/gerarTese/{ticker}")
async def gerar_tese(ticker: str, dados: DadosEntrada, session: AsyncSession = Depends(get_session)):
    controller = AIController(session)
    return await controller.get_tese(ticker.upper(), dados.model_dump())
