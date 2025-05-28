@echo off
REM Script para Windows - Windows Batch (.bat)
REM Cria .venv, instala dependências, inicializa banco e roda FastAPI

REM Verifica se .venv existe
if not exist ".venv" (
    echo Criando ambiente virtual...
    python -m venv .venv
) else (
    echo Ambiente virtual ja existe.
)

REM Ativa o ambiente virtual
call .venv\Scripts\activate.bat

REM Atualiza pip e instala requirements
echo Instalando dependencias...
pip install --upgrade pip
pip install -r requirements.txt

REM Inicializa o banco
echo Criando tabelas no banco de dados...
python app\init_db.py

REM Roda o servidor FastAPI
echo Iniciando servidor FastAPI...
call .venv\Scripts\fastapi.exe dev app\main.py
