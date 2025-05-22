# 📊 PalomaInvest – API de Consulta e Análise Fundamentalista de Ações

**PalomaInvest** é uma aplicação web desenvolvida em **Python** com **FastAPI**, projetada para disponibilizar dados fundamentalistas de ações listadas na B3. A aplicação coleta e organiza informações relevantes para análise de investimentos, oferecendo endpoints RESTful para consulta de empresas, setores, indicadores e modelos de valuation.

---

## 🚀 Funcionalidades

- 🔎 Consulta de empresas por ticker, setor ou subsetor  
- 📈 Retorno de múltiplos fundamentalistas com base nos dados do [Fundamentus](https://fundamentus.com.br/)  
- 💰 Cálculo de valor intrínseco usando modelos como:
  - Método de Décio Bazin
  - Modelo de Gordon (Dividend Discount Model)
  - Fórmula opiniada baseada em Graham
  - Fluxo de Caixa Descontado (DCF)  
- 🧠 Geração inicial de teses de investimento com **IA generativa Gemini**  
- 📄 Preparado para exportação em PDF das análises (em desenvolvimento)  
- 🧮 Simulador de juros compostos (frontend)

---

## 🧱 Tecnologias utilizadas

- **FastAPI** – framework web assíncrono
- **SQLAlchemy** – ORM para modelagem e queries no banco
- **PostgreSQL** – banco de dados relacional
- **fundamentus-api** – coleta de dados fundamentalistas via web scraping
- **Docker (local)** – para desenvolvimento com PostgreSQL
- **Render** – hospedagem gratuita da API e banco (planejado)
- **Gemini (IA)** – geração de teses de investimento

---

## 🗂 Estrutura do projeto

```
PalomaInvest/
│
├── project/
│   ├── config.py              # Configuração do banco (engine, session)
│   ├── models/                # Modelos ORM (Empresa, Setor, etc.)
│   │   └── __init__.py
│   ├── scripts/
│   │   └── popular_banco.py   # Script auxiliar para popular o banco em testes locais
│   ├── routes/                # Rotas da API (em breve)
│   └── __init__.py
│
├── main.py                    # Inicialização da aplicação FastAPI
├── requirements.txt
└── README.md
```

---

## 🧪 Como rodar localmente

### 1. Clone o projeto

```bash
git clone https://github.com/seuusuario/paloma-invest.git
cd paloma-invest
```

### 2. Crie o ambiente virtual e instale as dependências

```bash
python -m venv venv
source venv/bin/activate  # ou .\venv\Scripts\activate no Windows
pip install -r requirements.txt
```

### 3. Configure o PostgreSQL

Crie um banco chamado `paloma_normalizado` e atualize a variável `DATABASE_URL` no `config.py`:

```python
DATABASE_URL = "postgresql://postgres:SENHA@localhost:5432/paloma_normalizado"
```

### 4. Popule o banco com dados do Fundamentus (apenas para testes locais)

```bash
python project/scripts/popular_banco.py
```

> ⚠️ Este script é usado apenas durante o desenvolvimento. Na aplicação em produção, a população de dados será embutida e automatizada via API.

### 5. Rode a aplicação

```bash
uvicorn main:app --reload
```

A API estará disponível em: [http://127.0.0.1:8000](http://127.0.0.1:8000)

---

## 🔐 Segurança e limites

- A hospedagem gratuita no Render limita o banco de dados a **256 MB**
- Sem cartão de crédito cadastrado, **não há risco de cobranças inesperadas**
- Para uso produtivo ou aplicações comerciais, recomenda-se migrar para um plano pago

---

## 📱 Integração com outras plataformas

Este projeto está sendo preparado para consumo por:
- Aplicativos Android desenvolvidos com **Java**
- Interfaces web frontend (em breve)
- Possível uso como backend para dashboards financeiros

---

## 📌 Status do projeto

✅ Coleta e armazenamento de dados  
✅ Estrutura de banco normalizada  
✅ FastAPI funcionando localmente  
🧠 Geração de teses com IA (versão inicial funcional)  
⚙️ Em desenvolvimento: Rotas da API, exportação em PDF, frontend

---

## 📄 Licença

Este projeto está licenciado sob a **MIT License**.

---

## 🤝 Contribuição

Sinta-se à vontade para abrir issues, relatar bugs ou sugerir melhorias. Pull requests são bem-vindos!

---

by **Davi R.**  
