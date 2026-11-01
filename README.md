# 📈 Analisador Preditivo de Carteira: Monte Carlo + LLM

Este projeto em Python foi desenvolvido para analisar ações da bolsa brasileira (B3), estimar cenários futuros de preços e gerar relatórios explicativos automáticos usando Inteligência Artificial local.

O grande diferencial é a separação de responsabilidades: a matemática e a estatística ficam a cargo do Python, enquanto a interpretação contextual (notícias, cenário macroeconômico) é feita por uma LLM (Large Language Model) rodando localmente.

## ⚙️ Como funciona a arquitetura

O código foi modularizado para facilitar a manutenção e evolução:

*   **`main.py`**: O maestro do projeto. Lê a lista de ações, orquestra as chamadas matemáticas e de IA, e imprime o resultado final.
*   **`src/data_loader.py`**: Responsável por baixar os dados oficiais da B3 (via biblioteca `b3quant`). Ele faz o cache local (salvando em arquivos `.parquet`) para evitar downloads repetitivos e bloqueios de rede.
*   **`src/monte_carlo.py`**: O "cérebro matemático". Utiliza o modelo de Movimento Browniano Geométrico (GBM) e milhares de simulações para calcular probabilidades de alta, mediana de preços e o VaR (Value at Risk).
*   **`src/llm_report.py`**: O "cérebro interpretativo". Conecta-se ao Ollama (Llama 3) passando as métricas calculadas e o contexto atual para gerar uma explicação em linguagem natural.
*   **`skills_analista.txt`**: Arquivo externo que define a "persona" da IA. Aqui você pode mudar o tom de voz, pedir respostas mais curtas ou definir as regras do relatório sem precisar mexer no código Python.
*   **`tickers.txt`**: Lista de ações que você deseja analisar (uma por linha).

## 🛠️ Tecnologias Utilizadas
*   **Python** (Pandas, NumPy)
*   **b3quant** (Download de dados oficiais da B3)
*   **Ollama / Llama 3** (Inteligência Artificial Local)
*   **OpenAI Python Library** (Usada para conectar ao servidor local do Ollama)

## 🚀 Como executar este projeto

1. Clone o repositório e crie um ambiente virtual:
   ```bash
   python -m venv venv
   source venv/bin/activate
