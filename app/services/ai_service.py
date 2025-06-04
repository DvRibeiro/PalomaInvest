import math
import google.generativeai as genai
from app.services.acoes_service import AcoesService  # Reaproveite seu service de acoes

class AiService:

    def __init__(self, ticker, session):
        genai.configure(api_key="AIzaSyC1qCBg76qEnyTCkATqmNO8WuQJnr_eEwM")
        self.model = genai.GenerativeModel("gemini-2.0-flash")
        self.ticker = ticker
        self.session = session

    def get_texto_padrao(self):
        return """
            Você é um analista fundamentalista experiente. Crie uma tese de investimento para a ação {ticker}, com base nos seguintes dados:

            {dados}

            Valor intrínseco estimado: {valor_intrinseco}

            Siga este roteiro de análise:

            1. **Pontos fortes**: Destaque os indicadores positivos (ex: ROE alto, baixo endividamento, boa margem).
            2. **Pontos fracos**: Comente sobre riscos ou indicadores desfavoráveis (ex: crescimento baixo, alta dívida).
            3. **Avaliação atual**:
            - Compare o P/L com a média do setor.
            - Avalie se o Dividend Yield é atrativo considerando a taxa Selic (~10,5% a.a.).
            - Comente se o ROE indica boa eficiência.
            4. **Oportunidades e ameaças**:
            - Descreva o cenário do setor e como a empresa está posicionada.
            5. **Margem de segurança**:
            - Considere o valor intrínseco e o preço atual da ação.
            6. **Conclusão**:
            - A ação está subavaliada ou não?
            - Há potencial de valorização?
            - Recomendação: Comprar, manter em observação, ou evitar?

            Use linguagem clara, objetiva e acessível para investidores iniciantes, mas com argumentação técnica.
"""

    def calcula_valor_intrinseco(self, dados_usuario, dados_tese):
        lpa = dados_tese.get("lpa", 0)
        vpa = dados_tese.get("vpa", 0)

        try:
            if dados_usuario:
                constante = float(dados_usuario["pl"]) * float(dados_usuario["pvp"])
            else:
                constante = float(dados_tese["pl"]) * float(dados_tese["pvp"])
            vi = math.sqrt(constante * float(lpa) * float(vpa))
            return f"√(P/L * P/VP * LPA * VPA) = R$ {vi:.2f}"
        except Exception:
            return "Não foi possível calcular o valor intrínseco."

    async def filtrar_indicadores_tese(self):
        try:
            service = AcoesService(self.session)
            dados = await service.get_acao_detalhes(self.ticker)

            indicadores_map = {d["nome"].lower().replace(" ", "_"): d["valor"] for d in dados.get("indicadores", [])}

            campos_relevantes = [
                "codigo_acao", "nome_empresa", "setor",
                "cotacao", "pl", "pvp", "dividend_yield", "roe",
                "lucro_liquido_12m", "crescimento_receita_5_anos", "patrimonio_liquido",
                "valor_de_mercado", "ativo", "vpa", "lpa"
            ]

            dados_filtrados = {campo: indicadores_map.get(campo) for campo in campos_relevantes}
            dados_filtrados["codigo"] = dados.get("codigo_acao")
            dados_filtrados["nome_empresa"] = dados.get("nome_empresa")
            dados_filtrados["setor"] = dados.get("setor")

            return dados_filtrados
        except Exception as e:
            return {"status": "error", "message": str(e)}

class AI:
    def __init__(self, ticker, session):
        self.service = AiService(ticker, session)

    async def gerar_tese(self, dados_usuario):
        dados_tese = await self.service.filtrar_indicadores_tese()

        dados_formatados = "\n".join(
            f"- {campo.replace('_', ' ').capitalize()}: {valor}"
            for campo, valor in dados_tese.items()
        )

        valor_intrinseco = self.service.calcula_valor_intrinseco(dados_usuario, dados_tese)        

        texto_padrao = self.service.get_texto_padrao().format(
            ticker=self.service.ticker,
            dados=dados_formatados,
            valor_intrinseco=valor_intrinseco
        )

        try:
            resposta = self.service.model.generate_content(texto_padrao)
            return {
                "vi": valor_intrinseco,
                "tese": resposta.text,
                "dados": dados_tese,
                "prompt": texto_padrao
            }
        except Exception as e:
            return {"status": "error", "message": f"Erro ao gerar conteúdo com IA: {e}"}
