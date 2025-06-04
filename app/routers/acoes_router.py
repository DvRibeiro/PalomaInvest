from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.controllers.acoes_controller import AcoesController
from app.config.DBconfig import get_session  # sua dependência que fornece AsyncSession

router = APIRouter()

@router.get("/")
async def home(session: AsyncSession = Depends(get_session)):
    controller = AcoesController(session)
    return await controller.home()

@router.get("/detalhes/")
async def list_all_acoes_indicadores(session: AsyncSession = Depends(get_session)):
    controller = AcoesController(session)
    return await controller.list_all_acoes_indicadores()

@router.get("/acoes/{ticker}")
async def get_acao(ticker: str, session: AsyncSession = Depends(get_session)):
    controller = AcoesController(session)
    return await controller.get_acao(ticker)

@router.get("/acoes/detalhes/{ticker}")
async def get_acao_detalhes(ticker: str, session: AsyncSession = Depends(get_session)):
    controller = AcoesController(session)
    return await controller.get_acao_detalhes(ticker)

@router.get("/api/acoes/historico")
async def get_indicador_historico(session: AsyncSession = Depends(get_session)):
    controller = AcoesController(session)
    return await controller.get_indicador_historico()
