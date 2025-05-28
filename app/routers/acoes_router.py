from fastapi import APIRouter
from app.controllers.acoes_controller import AcoesController

acoes = AcoesController()
router = APIRouter()

@router.get("/")
async def home():
    return await acoes.home()

@router.get("/detalhes/")
async def list_all_acoes_indicadores():
    return await acoes.list_all_acoes_indicadores()

@router.get("/acoes/{ticker}")
async def get_acao(ticker: int):
    return await acoes.get_acao(ticker)

@router.get("/acoes/detalhes/{ticker}")
async def get_acao_detalhes(ticker: int):
    return await acoes.get_acao_detalhes(ticker)

@router.get("/api/acoes/historico")
async def get_indicador_historico():
    return await acoes.get_indicador_historico()
