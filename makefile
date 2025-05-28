# Makefile

PYTHON := .venv/bin/python
PIP := .venv/bin/pip
ENTRYPOINT := app/main.py
INIT_SCRIPT := app/init_db.py

# Define o PYTHONPATH para reconhecer os módulos corretamente
export PYTHONPATH := .

.PHONY: venv install init run all clean

## Cria o ambiente virtual (.venv) se não existir
venv:
	@echo "🐍 Criando ambiente virtual..."
	@test -d .venv || python3 -m venv .venv

## Instala as dependências no ambiente virtual
install: venv
	@echo "📦 Instalando dependências no .venv..."
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt

## Inicializa o banco com SQLAlchemy
init:
	@echo "🗃️ Criando tabelas no banco de dados..."
	$(PYTHON) $(INIT_SCRIPT)

## Roda o servidor FastAPI com live reload
run:
	@echo "🚀 Iniciando servidor FastAPI com reload..."
	.venv/bin/fastapi dev $(ENTRYPOINT)

## Tudo: cria venv, instala, inicializa banco e roda API
all: install init run

## Limpa arquivos .pyc e __pycache__
clean:
	@echo "🧹 Limpando arquivos temporários..."
	find . -type d -name '__pycache__' -exec rm -r {} +
	find . -type f -name '*.pyc' -delete
