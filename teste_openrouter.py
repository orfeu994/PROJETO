from openai import OpenAI

# Configurando o cliente para o Ollama local
client = OpenAI(
    base_url="http://localhost:11434/v1",
    api_key="ollama",
)

# 1. Simulando os dados que o seu código de Monte Carlo vai gerar
metricas = {
    "ticker": "PETR4",
    "preco_atual": 38.50,
    "mediana_1ano": 41.20,
    "p5": 28.30,
    "p95": 56.80,
    "prob_alta": 0.63,
    "var_95": -0.26,
}

# 2. Simulando o contexto que você vai coletar (notícias/macro)
contexto = "Ano eleitoral. Notícias recentes falam sobre mudança na política de preços de combustíveis."

# 3. Montando o Prompt (O Segredo do Sucesso)
prompt = f"""
Você é um analista financeiro explicando resultados para um investidor iniciante.
NÃO faça previsões. Apenas interprete os dados abaixo.

DADOS DA SIMULAÇÃO (Monte Carlo, horizonte 1 ano):
- Ação: {metricas['ticker']}
- Preço atual: R$ {metricas['preco_atual']:.2f}
- Mediana projetada: R$ {metricas['mediana_1ano']:.2f}
- Intervalo de 90% de confiança: R$ {metricas['p5']:.2f} a R$ {metricas['p95']:.2f}
- Probabilidade de alta: {metricas['prob_alta']:.1%}
- VaR 95%: {metricas['var_95']:.1%}

CONTEXTO EXTRA:
{contexto}

TAREFA:
Explique, em até 150 palavras:
1. O que o intervalo de confiança e a probabilidade de alta significam na prática.
2. Como o contexto extra pode explicar a volatilidade observada.
3. Quais riscos o investidor deve monitorar.
"""

print("Analisando dados e gerando relatório (isso pode demorar alguns segundos)...\n")

# 4. Chamando a LLM local
try:
    resposta = client.chat.completions.create(
        model="llama3",
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
        max_tokens=500
    )
    
    print("--- RELATÓRIO DA LLM ---")
    print(resposta.choices[0].message.content)
    print("------------------------")

except Exception as e:
    print(f"Deu erro: {e}")