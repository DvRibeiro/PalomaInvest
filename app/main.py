from fastapi import FastAPI
from app.routers import acoes_router, ai_router

app = FastAPI()

app.include_router(acoes_router.router)
app.include_router(ai_router.router)