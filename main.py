from src.data_loader import carregar_ticker
from src.monte_carlo import gerar_metricas
from src.llm_report import gerar_relatorio_ia

def main():
    contexto = "Ano eleitoral. Discussões sobre política de preços e juros."
    
    try:
        with open("tickers.txt", "r", encoding="utf-8") as f:
            tickers = [linha.strip() for linha in f if linha.strip()]
    except FileNotFoundError:
        print("Erro: Arquivo tickers.txt não encontrado.")
        return

    for ticker in tickers:
        print(f"\n{'='*40}")
        print(f"🔍 ANALISANDO: {ticker}")
        print(f"{'='*40}")
        
        try:
            # 1. Carrega os dados (Últimos 12 meses)
            dados = carregar_ticker(ticker, meses_historico=12)
            
            # 2. Roda o Monte Carlo
            metricas = gerar_metricas(ticker, dados)
            print(f"Preço Atual: R$ {metricas['preco_atual']:.2f}")
            print(f"Mediana Projetada: R$ {metricas['mediana_1ano']:.2f}")
            print(f"Probabilidade de Alta: {metricas['prob_alta']:.1%}")
            
            # 3. Gera o relatório com a IA
            print("\n⏳ Gerando relatório com a IA local (Llama 3)...")
            relatorio = gerar_relatorio_ia(metricas, contexto)
            
            print("\n📝 RELATÓRIO:")
            print(relatorio)
            
        except ValueError as e:
            print(f"❌ Erro de dados: {e}")
        except Exception as e:
            print(f"❌ Erro inesperado: {e}")

if __name__ == "__main__":
    main()