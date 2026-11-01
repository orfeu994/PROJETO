from openai import OpenAI

def gerar_relatorio_ia(metricas, contexto=""):
    with open("skills_analista.txt", "r", encoding="utf-8") as file:
        system_prompt = file.read()

    user_prompt = f"""
    DADOS DA SIMULAÇÃO:
    - Ação: {metricas['ticker']}
    - Preço atual: R$ {metricas['preco_atual']:.2f}
    - Mediana projetada: R$ {metricas['mediana_1ano']:.2f}
    - Intervalo 90%: R$ {metricas['p5']:.2f} a R$ {metricas['p95']:.2f}
    - Probabilidade de alta: {metricas['prob_alta']:.1%}
    - VaR 95%: {metricas['var_95']:.1%}
    
    CONTEXTO EXTRA: {contexto}
    """

    client = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")
    
    resposta = client.chat.completions.create(
        model="llama3",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0.3
    )
    
    return resposta.choices[0].message.content