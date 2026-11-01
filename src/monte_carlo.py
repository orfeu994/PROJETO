import numpy as np

def gerar_metricas(ticker, dados, dias=252, n_simulacoes=10000):
    precos = dados['close'].dropna()
    
    if precos.empty:
        raise ValueError(f"Preços vazios para {ticker}.")

    preco_atual = float(precos.iloc[-1])
    
    retornos = np.log(precos / precos.shift(1)).dropna()
    mu = float(retornos.mean() * 252)
    sigma = float(retornos.std() * np.sqrt(252))
    
    Z = np.random.normal(0, 1, (dias, n_simulacoes))
    retornos_diarios = np.exp((mu - 0.5 * sigma**2) * (1/252) + sigma * np.sqrt(1/252) * Z)
    
    caminhos = np.zeros((dias + 1, n_simulacoes))
    caminhos[0] = preco_atual
    caminhos[1:] = preco_atual * np.cumprod(retornos_diarios, axis=0)
    
    precos_finais = caminhos[-1]
    
    return {
        "ticker": ticker,
        "preco_atual": preco_atual,
        "mediana_1ano": float(np.median(precos_finais)),
        "p5": float(np.percentile(precos_finais, 5)),
        "p95": float(np.percentile(precos_finais, 95)),
        "prob_alta": float(np.mean(precos_finais > preco_atual)),
        "var_95": float((np.percentile(precos_finais, 5) / preco_atual) - 1)
    }