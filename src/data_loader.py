import b3quant as pyb
import pandas as pd
import os
from datetime import datetime
from dateutil.relativedelta import relativedelta

def carregar_ticker(ticker, meses_historico=12):
    hoje = datetime.now()
    data_fim = hoje.replace(day=1) - relativedelta(days=1)
    data_inicio = data_fim - relativedelta(months=meses_historico)
    
    meses_necessarios = []
    ano_atual, mes_atual = data_inicio.year, data_inicio.month
    while (ano_atual, mes_atual) <= (data_fim.year, data_fim.month):
        meses_necessarios.append((ano_atual, mes_atual))
        if mes_atual == 12:
            ano_atual += 1
            mes_atual = 1
        else:
            mes_atual += 1

    os.makedirs("data", exist_ok=True)
    dfs = []
    
    for ano, mes in meses_necessarios:
        cache_file = f"data/cotahist_{ano}_{mes:02d}.parquet"
        
        if os.path.exists(cache_file):
            df_mes = pd.read_parquet(cache_file)
        else:
            print(f"Baixando base oficial da B3: {mes:02d}/{ano}... (Aguarde)")
            try:
                df_mes = pyb.get_stocks(year=ano, month=mes)
                df_mes.to_parquet(cache_file)
            except Exception as e:
                print(f"⚠️ Falha ao baixar {mes:02d}/{ano}: {e}")
                continue
        
        if df_mes is not None and not df_mes.empty:
            dfs.append(df_mes)
    
    if not dfs:
        raise ValueError(f"Nenhum dado foi baixado para o período solicitado.")

    df = pd.concat(dfs, ignore_index=True)
    
    # --- AQUI ESTÁ A CORREÇÃO DOS NOMES DAS COLUNAS ---
    # Renomeia 'trade_date' para 'date' e 'close_price' para 'close'
    df.rename(columns={'trade_date': 'date', 'close_price': 'close'}, inplace=True)
    
    # Garante que os nomes fiquem em minúsculo (por segurança)
    df.columns = [c.lower() for c in df.columns]
    
    if 'date' not in df.columns:
        raise ValueError("A coluna 'date' não foi encontrada nos dados da B3 após a renomeação.")

    df['date'] = pd.to_datetime(df['date'])
    df = df[(df['date'] >= data_inicio) & (df['date'] <= data_fim)]
    
    ticker_limpo = ticker.replace('.SA', '')
    df_ticker = df[df['ticker'] == ticker_limpo].copy()
    
    if df_ticker.empty:
        raise ValueError(f"Dados não encontrados para {ticker_limpo} no período de {meses_historico} meses.")
        
    return df_ticker.sort_values('date')