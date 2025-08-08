# Explicação do Algoritmo de Análise de Vendas - Loja Bemol

Este documento explica linha por linha o código Python criado para analisar os dados de vendas da Loja Bemol. O objetivo é tornar o código compreensível para pessoas sem conhecimento técnico em programação.

## 📚 Importação das Bibliotecas (Linhas 1-7)

```python
import pandas as pd
```
**O que faz:** Importa a biblioteca pandas e dá a ela o apelido "pd". O pandas é como uma ferramenta poderosa para trabalhar com tabelas de dados (como Excel, mas no Python).

```python
import numpy as np
```
**O que faz:** Importa a biblioteca numpy com apelido "np". É uma ferramenta para fazer cálculos matemáticos complexos de forma rápida.

```python
import matplotlib.pyplot as plt
```
**O que faz:** Importa uma ferramenta para criar gráficos bonitos (como gráficos de barras, linhas, etc.).

```python
import seaborn as sns
```
**O que faz:** Importa outra ferramenta para fazer gráficos ainda mais bonitos e profissionais.

```python
from datetime import datetime, timedelta
```
**O que faz:** Importa ferramentas para trabalhar com datas (como calcular "há 12 meses atrás").

```python
import warnings
warnings.filterwarnings('ignore')
```
**O que faz:** Desliga mensagens de aviso chatas que o Python às vezes mostra, mas que não são importantes para nós.

## 🔧 Função para Carregar os Dados (Linhas 9-20)

```python
def carregar_dados():
```
**O que faz:** Cria uma "receita" (função) chamada "carregar_dados" que vamos usar para abrir e preparar nossos dados.

```python
    """Carrega e prepara os dados da base de vendas."""
```
**O que faz:** É um comentário explicando o que esta função faz. Como uma nota para lembrar.

```python
    df = pd.read_excel('base_vendas.xlsx')
```
**O que faz:** Abre o arquivo Excel chamado "base_vendas.xlsx" e coloca todos os dados numa variável chamada "df" (como uma tabela gigante na memória do computador).

```python
    df['Data_compra'] = pd.to_datetime(df['Data_compra'])
```
**O que faz:** Pega a coluna "Data_compra" e garante que o Python entenda que são datas de verdade (não apenas texto).

```python
    df['Ano'] = df['Data_compra'].dt.year
```
**O que faz:** Cria uma nova coluna chamada "Ano" extraindo apenas o ano de cada data (ex: de "2023-05-15" pega apenas "2023").

```python
    df['Mes'] = df['Data_compra'].dt.month
```
**O que faz:** Cria uma nova coluna chamada "Mes" extraindo apenas o mês de cada data (ex: de "2023-05-15" pega apenas "5").

```python
    df['Ano_Mes'] = df['Data_compra'].dt.to_period('M')
```
**O que faz:** Cria uma nova coluna que junta ano e mês (ex: "2023-05") para facilitar análises mensais.

```python
    return df
```
**O que faz:** Devolve a tabela preparada para quem pediu.

## 🥇 Pergunta 1: Produto Mais Vendido (Linhas 22-52)

```python
def pergunta_1(df):
```
**O que faz:** Cria uma nova função para responder a primeira pergunta.

```python
    print("=" * 80)
    print("PERGUNTA 1: Produto mais vendido (últimos 12 meses)")
    print("=" * 80)
```
**O que faz:** Imprime um título bonito na tela para organizar os resultados.

```python
    data_limite = df['Data_compra'].max() - timedelta(days=365)
```
**O que faz:** Calcula qual foi a data de exatamente 1 ano atrás (365 dias) a partir da data mais recente nos dados.

```python
    df_12m = df[df['Data_compra'] >= data_limite]
```
**O que faz:** Cria uma nova tabela contendo apenas as vendas dos últimos 12 meses.

```python
    vendas_produto = df_12m.groupby('Produto').agg({
        'Valor Total': 'sum',
        'Qtd': 'count',
        'Unidade': 'nunique'
    }).reset_index()
```
**O que faz:** 
- Agrupa os dados por produto
- Para cada produto, calcula: soma do valor total vendido, quantidade de vendas realizadas, e em quantas unidades diferentes foi vendido
- É como fazer uma planilha resumo por produto

```python
    produtos_filtrados = vendas_produto[
        (vendas_produto['Qtd'] >= 50) & 
        (vendas_produto['Unidade'] >= 3)
    ]
```
**O que faz:** Filtra apenas produtos que tiveram pelo menos 50 vendas E foram vendidos em pelo menos 3 unidades diferentes.

```python
    if len(produtos_filtrados) > 0:
        produto_top = produtos_filtrados.loc[produtos_filtrados['Valor Total'].idxmax()]
```
**O que faz:** Se existirem produtos que atendem aos critérios, encontra aquele com maior valor total de vendas.

```python
        print(f"Produto: {produto_top['Produto']}")
        print(f"Receita Total: R$ {produto_top['Valor Total']:,.2f}")
        print(f"Número de Vendas: {produto_top['Qtd']}")
        print(f"Unidades que vendem: {produto_top['Unidade']}")
```
**O que faz:** Mostra na tela as informações do produto vencedor de forma organizada.

## 💰 Pergunta 2: Ticket Médio por Vendedor (Linhas 54-77)

```python
def pergunta_2(df):
```
**O que faz:** Cria função para a segunda pergunta.

```python
    ticket_vendedor = df.groupby('Cod_vendedor').agg({
        'Valor Total': ['mean', 'count']
    }).round(2)
```
**O que faz:** Para cada vendedor, calcula a média dos valores das vendas (ticket médio) e conta quantas vendas fez.

```python
    ticket_vendedor.columns = ['Ticket_Medio', 'Num_Vendas']
```
**O que faz:** Renomeia as colunas para nomes mais claros.

```python
    vendedor_top = ticket_vendedor.loc[ticket_vendedor['Ticket_Medio'].idxmax()]
```
**O que faz:** Encontra o vendedor com o maior ticket médio.

## 🏆 Pergunta 3: Maior Ticket Médio (Linhas 79-91)

```python
def pergunta_3(df):
```
**O que faz:** Função para a terceira pergunta (bem simples).

```python
    ticket_vendedor = df.groupby('Cod_vendedor')['Valor Total'].mean()
    maior_ticket = ticket_vendedor.max()
```
**O que faz:** Calcula o ticket médio de cada vendedor e pega o maior valor.

## 📈 Pergunta 4: Crescimento por Unidade (Linhas 93-130)

```python
def pergunta_4(df):
```
**O que faz:** Função para analisar crescimento das vendas.

```python
    vendas_anuais = df.groupby(['Unidade', 'Categoria', 'Ano'])['Valor Total'].sum().reset_index()
```
**O que faz:** Agrupa vendas por unidade, categoria e ano, somando os valores.

```python
    crescimento_unidades = []
```
**O que faz:** Cria uma lista vazia para guardar os resultados de crescimento.

```python
    for unidade in df['Unidade'].unique():
```
**O que faz:** Para cada unidade da loja, vai calcular o crescimento.

```python
        vendas_unidade = df[df['Unidade'] == unidade].groupby('Ano')['Valor Total'].sum()
```
**O que faz:** Pega as vendas totais por ano para a unidade atual.

```python
        if len(vendas_unidade) > 1:
```
**O que faz:** Só calcula crescimento se a unidade teve vendas em mais de um ano.

```python
            for i in range(1, len(anos)):
                ano_anterior = vendas_unidade[anos[i-1]]
                ano_atual = vendas_unidade[anos[i]]
                
                if ano_anterior > 0:
                    crescimento = ((ano_atual - ano_anterior) / ano_anterior) * 100
```
**O que faz:** Para cada par de anos consecutivos, calcula o percentual de crescimento usando a fórmula: ((ano atual - ano anterior) / ano anterior) × 100.

## 🥧 Pergunta 5: Participação das Unidades (Linhas 132-152)

```python
def pergunta_5(df):
```
**O que faz:** Função para calcular participação percentual.

```python
    faturamento_unidade = df.groupby('Unidade')['Valor Total'].sum()
    faturamento_total = df['Valor Total'].sum()
```
**O que faz:** Calcula quanto cada unidade faturou e o faturamento total da empresa.

```python
    participacao = (faturamento_unidade / faturamento_total * 100).round(2)
```
**O que faz:** Calcula a porcentagem que cada unidade representa do total: (faturamento da unidade ÷ faturamento total) × 100.

## 💲 Pergunta 6: Simulação de Aumento (Linhas 154-184)

```python
def pergunta_6(df):
```
**O que faz:** Função para simular cenário de aumento de preços.

```python
    df_simulacao = df.copy()
```
**O que faz:** Cria uma cópia dos dados para não alterar os originais.

```python
    moveis_baixo = (df_simulacao['Categoria'] == 'Móveis') & (df_simulacao['Valor Unitário'] < 1500)
    informatica_baixo = (df_simulacao['Categoria'] == 'Informática') & (df_simulacao['Valor Unitário'] < 1500)
```
**O que faz:** Identifica quais produtos são de móveis ou informática com preço abaixo de R$ 1500.

```python
    df_simulacao.loc[moveis_baixo, 'Valor Unitário'] *= 1.10
    df_simulacao.loc[informatica_baixo, 'Valor Unitário'] *= 1.15
```
**O que faz:** Aumenta preço dos móveis em 10% (×1.10) e informática em 15% (×1.15).

```python
    df_simulacao['Valor Total'] = df_simulacao['Valor Unitário'] * df_simulacao['Qtd']
```
**O que faz:** Recalcula o valor total das vendas com os novos preços.

## 🏪 Pergunta 7: Faturamento Acumulado (Linhas 186-208)

```python
def pergunta_7(df):
```
**O que faz:** Função para encontrar unidade com maior faturamento acumulado.

```python
    faturamento_mensal = df.groupby(['Unidade', 'Ano_Mes'])['Valor Total'].sum().reset_index()
```
**O que faz:** Calcula faturamento mensal de cada unidade.

```python
    for unidade in df['Unidade'].unique():
        dados_unidade = faturamento_mensal[faturamento_mensal['Unidade'] == unidade].sort_values('Ano_Mes')
        dados_unidade['Faturamento_Acumulado'] = dados_unidade['Valor Total'].cumsum()
```
**O que faz:** Para cada unidade, ordena por mês e calcula faturamento acumulado (soma progressiva mês a mês).

## ⚠️ Pergunta 8: Detecção de Anomalias (Linhas 210-246)

```python
def pergunta_8(df):
```
**O que faz:** Função para encontrar dados estranhos (anomalias).

```python
    Q1_valor = df['Valor Unitário'].quantile(0.25)
    Q3_valor = df['Valor Unitário'].quantile(0.75)
    IQR_valor = Q3_valor - Q1_valor
```
**O que faz:** Calcula quartis (divisões dos dados em 4 partes iguais) para identificar valores extremos.

```python
    limite_inf_valor = Q1_valor - 1.5 * IQR_valor
    limite_sup_valor = Q3_valor + 1.5 * IQR_valor
```
**O que faz:** Define limites: valores muito abaixo ou muito acima destes limites são considerados anômalos.

```python
    anomalias_valor = (df['Valor Unitário'] < limite_inf_valor) | (df['Valor Unitário'] > limite_sup_valor)
    anomalias_qtd = df['Qtd'] > limite_sup_qtd
```
**O que faz:** Marca como anomalia valores unitários muito baixos/altos OU quantidades excessivamente altas.

## 🔗 Pergunta 9: Correlação (Linhas 248-276)

```python
def pergunta_9(df):
```
**O que faz:** Função para analisar relações entre variáveis.

```python
    df_numeric = df.select_dtypes(include=[np.number])
```
**O que faz:** Seleciona apenas colunas com números (não texto).

```python
    correlacao = df_numeric.corr()
```
**O que faz:** Calcula correlação: mede se quando uma variável aumenta, outra também aumenta (correlação positiva) ou diminui (correlação negativa).

```python
    if abs(corr_value) > 0.5:
```
**O que faz:** Considera correlação significativa quando o valor é maior que 0.5 (correlação moderada a forte).

## 📊 Pergunta 10: Consistência de Vendedores (Linhas 278-308)

```python
def pergunta_10(df):
```
**O que faz:** Função para encontrar vendedor mais consistente.

```python
    stats_vendedor = df.groupby('Cod_vendedor').agg({
        'Valor Total': ['count', 'std', 'mean']
    }).round(2)
```
**O que faz:** Para cada vendedor calcula: quantidade de vendas, desvio padrão e média.

```python
    vendedores_filtrados = stats_vendedor[stats_vendedor['Num_Vendas'] >= 5]
```
**O que faz:** Considera apenas vendedores com pelo menos 5 vendas.

```python
    vendedor_consistente = vendedores_filtrados.loc[vendedores_filtrados['Desvio_Padrao'].idxmin()]
```
**O que faz:** Encontra o vendedor com menor desvio padrão (vendas mais consistentes, sem muita variação).

## 🚀 Função Principal (Linhas 310-330)

```python
def main():
```
**O que faz:** Função principal que coordena tudo.

```python
    df = carregar_dados()
```
**O que faz:** Carrega os dados usando nossa função.

```python
    pergunta_1(df)
    pergunta_2(df)
    # ... todas as outras perguntas
```
**O que faz:** Executa todas as funções de perguntas em sequência.

```python
if __name__ == "__main__":
    main()
```
**O que faz:** Se este arquivo for executado diretamente (não importado), executa a função main(). É como apertar o botão "iniciar" do programa.

---

## 🎯 Resumo Geral

Este algoritmo é como uma máquina de análise que:

1. **Carrega** dados de vendas de um arquivo Excel
2. **Limpa e prepara** os dados para análise
3. **Responde 10 perguntas** específicas sobre o negócio
4. **Calcula estatísticas** como médias, crescimento, correlações
5. **Identifica padrões** como anomalias e tendências
6. **Apresenta resultados** de forma organizada

Cada função é como um "mini-programa" especializado em resolver uma pergunta específica, e todas trabalham juntas para fornecer uma análise completa dos dados de vendas da Loja Bemol. 