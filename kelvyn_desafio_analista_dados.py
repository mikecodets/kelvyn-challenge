import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

def carregar_dados():
    """Carrega e prepara os dados da base de vendas."""
    df = pd.read_excel('base_vendas.xlsx')
    
    # Garantir que a coluna de data está no formato correto
    df['Data_compra'] = pd.to_datetime(df['Data_compra'])
    
    # Criar colunas auxiliares
    df['Ano'] = df['Data_compra'].dt.year
    df['Mes'] = df['Data_compra'].dt.month
    df['Ano_Mes'] = df['Data_compra'].dt.to_period('M')
    
    return df

def pergunta_1(df):
    """
    Qual é o produto mais vendido em termos de receita total nos últimos 12 meses,
    considerando apenas produtos que tiveram pelo menos 50 vendas e foram vendidos
    em pelo menos 3 unidades diferentes?
    """
    print("=" * 80)
    print("PERGUNTA 1: Produto mais vendido (últimos 12 meses)")
    print("=" * 80)
    
    # Calcular data limite (últimos 12 meses)
    data_limite = df['Data_compra'].max() - timedelta(days=365)
    df_12m = df[df['Data_compra'] >= data_limite]
    
    # Agrupar por produto
    vendas_produto = df_12m.groupby('Produto').agg({
        'Valor Total': 'sum',
        'Qtd': 'count',  # Número de vendas
        'Unidade': 'nunique'  # Número de unidades diferentes
    }).reset_index()
    
    # Aplicar filtros
    produtos_filtrados = vendas_produto[
        (vendas_produto['Qtd'] >= 50) & 
        (vendas_produto['Unidade'] >= 3)
    ]
    
    if len(produtos_filtrados) > 0:
        produto_top = produtos_filtrados.loc[produtos_filtrados['Valor Total'].idxmax()]
        print(f"Produto: {produto_top['Produto']}")
        print(f"Receita Total: R$ {produto_top['Valor Total']:,.2f}")
        print(f"Número de Vendas: {produto_top['Qtd']}")
        print(f"Unidades que vendem: {produto_top['Unidade']}")
    else:
        print("Nenhum produto atende aos critérios especificados")
    
    return produtos_filtrados

def pergunta_2(df):
    """
    Calcule o ticket médio por Cod_vendedor e identifique o Cod_vendedor 
    com o maior ticket médio.
    """
    print("\n" + "=" * 80)
    print("PERGUNTA 2: Ticket médio por vendedor")
    print("=" * 80)
    
    ticket_vendedor = df.groupby('Cod_vendedor').agg({
        'Valor Total': ['mean', 'count']
    }).round(2)
    
    ticket_vendedor.columns = ['Ticket_Medio', 'Num_Vendas']
    ticket_vendedor = ticket_vendedor.reset_index()
    
    vendedor_top = ticket_vendedor.loc[ticket_vendedor['Ticket_Medio'].idxmax()]
    
    print(f"Vendedor com maior ticket médio:")
    print(f"Código: {vendedor_top['Cod_vendedor']}")
    print(f"Ticket Médio: R$ {vendedor_top['Ticket_Medio']:,.2f}")
    print(f"Número de Vendas: {vendedor_top['Num_Vendas']}")
    
    return ticket_vendedor

def pergunta_3(df):
    """
    Identificar o maior valor do ticket médio.
    """
    print("\n" + "=" * 80)
    print("PERGUNTA 3: Maior valor do ticket médio")
    print("=" * 80)
    
    ticket_vendedor = df.groupby('Cod_vendedor')['Valor Total'].mean()
    maior_ticket = ticket_vendedor.max()
    
    print(f"Maior valor do ticket médio: R$ {maior_ticket:,.2f}")
    
    return maior_ticket

def pergunta_4(df):
    """
    Avalie a tendência de vendas de cada categoria ao longo do tempo,
    segmentando por unidade. Identifique a unidade com o maior crescimento
    percentual em vendas ano a ano.
    """
    print("\n" + "=" * 80)
    print("PERGUNTA 4: Tendência de vendas e crescimento por unidade")
    print("=" * 80)
    
    # Vendas por unidade, categoria e ano
    vendas_anuais = df.groupby(['Unidade', 'Categoria', 'Ano'])['Valor Total'].sum().reset_index()
    
    # Calcular crescimento ano a ano por unidade
    crescimento_unidades = []
    
    for unidade in df['Unidade'].unique():
        vendas_unidade = df[df['Unidade'] == unidade].groupby('Ano')['Valor Total'].sum()
        
        if len(vendas_unidade) > 1:
            anos = sorted(vendas_unidade.index)
            crescimentos = []
            
            for i in range(1, len(anos)):
                ano_anterior = vendas_unidade[anos[i-1]]
                ano_atual = vendas_unidade[anos[i]]
                
                if ano_anterior > 0:
                    crescimento = ((ano_atual - ano_anterior) / ano_anterior) * 100
                    crescimentos.append(crescimento)
            
            if crescimentos:
                crescimento_medio = np.mean(crescimentos)
                crescimento_unidades.append({
                    'Unidade': unidade,
                    'Crescimento_Medio_Anual': crescimento_medio
                })
    
    if crescimento_unidades:
        df_crescimento = pd.DataFrame(crescimento_unidades)
        unidade_maior_crescimento = df_crescimento.loc[df_crescimento['Crescimento_Medio_Anual'].idxmax()]
        
        print(f"Unidade com maior crescimento percentual:")
        print(f"Unidade: {unidade_maior_crescimento['Unidade']}")
        print(f"Crescimento médio anual: {unidade_maior_crescimento['Crescimento_Medio_Anual']:.2f}%")
        
        return df_crescimento
    else:
        print("Não foi possível calcular crescimento (dados insuficientes)")
        return pd.DataFrame()

def pergunta_5(df):
    """
    Crie um relatório que analise a participação percentual de cada unidade
    no faturamento total, destacando a unidade com a maior e a menor participação.
    """
    print("\n" + "=" * 80)
    print("PERGUNTA 5: Participação percentual das unidades no faturamento")
    print("=" * 80)
    
    faturamento_unidade = df.groupby('Unidade')['Valor Total'].sum()
    faturamento_total = df['Valor Total'].sum()
    
    participacao = (faturamento_unidade / faturamento_total * 100).round(2)
    participacao = participacao.sort_values(ascending=False)
    
    print("Participação percentual por unidade:")
    for unidade, percent in participacao.items():
        print(f"{unidade}: {percent:.2f}%")
    
    print(f"\nMaior participação: {participacao.index[0]} ({participacao.iloc[0]:.2f}%)")
    print(f"Menor participação: {participacao.index[-1]} ({participacao.iloc[-1]:.2f}%)")
    
    return participacao

def pergunta_6(df):
    """
    Simule um cenário onde os valores unitários de todos os produtos das
    categorias móveis e informática abaixo de R$1500,00 aumentem em 10% e 15%,
    respectivamente. Calcule o impacto no faturamento total.
    """
    print("\n" + "=" * 80)
    print("PERGUNTA 6: Simulação de aumento de preços")
    print("=" * 80)
    
    df_simulacao = df.copy()
    
    # Identificar produtos para aumento
    moveis_baixo = (df_simulacao['Categoria'] == 'Móveis') & (df_simulacao['Valor Unitário'] < 1500)
    informatica_baixo = (df_simulacao['Categoria'] == 'Informática') & (df_simulacao['Valor Unitário'] < 1500)
    
    # Aplicar aumentos
    df_simulacao.loc[moveis_baixo, 'Valor Unitário'] *= 1.10  # Aumento de 10%
    df_simulacao.loc[informatica_baixo, 'Valor Unitário'] *= 1.15  # Aumento de 15%
    
    # Recalcular valor total
    df_simulacao['Valor Total'] = df_simulacao['Valor Unitário'] * df_simulacao['Qtd']
    
    faturamento_original = df['Valor Total'].sum()
    faturamento_simulado = df_simulacao['Valor Total'].sum()
    impacto = faturamento_simulado - faturamento_original
    percentual_impacto = (impacto / faturamento_original) * 100
    
    print(f"Faturamento original: R$ {faturamento_original:,.2f}")
    print(f"Faturamento simulado: R$ {faturamento_simulado:,.2f}")
    print(f"Impacto no faturamento: R$ {impacto:,.2f}")
    print(f"Percentual de impacto: {percentual_impacto:.2f}%")
    
    return {'original': faturamento_original, 'simulado': faturamento_simulado, 'impacto': impacto}

def pergunta_7(df):
    """
    Qual unidade registrou o maior faturamento acumulado ao longo dos meses,
    com base na data de compra?
    """
    print("\n" + "=" * 80)
    print("PERGUNTA 7: Unidade com maior faturamento acumulado")
    print("=" * 80)
    
    faturamento_mensal = df.groupby(['Unidade', 'Ano_Mes'])['Valor Total'].sum().reset_index()
    
    # Calcular faturamento acumulado para cada unidade
    faturamento_acumulado = {}
    
    for unidade in df['Unidade'].unique():
        dados_unidade = faturamento_mensal[faturamento_mensal['Unidade'] == unidade].sort_values('Ano_Mes')
        dados_unidade['Faturamento_Acumulado'] = dados_unidade['Valor Total'].cumsum()
        faturamento_final = dados_unidade['Faturamento_Acumulado'].iloc[-1]
        faturamento_acumulado[unidade] = faturamento_final
    
    unidade_maior_faturamento = max(faturamento_acumulado, key=faturamento_acumulado.get)
    valor_maior = faturamento_acumulado[unidade_maior_faturamento]
    
    print(f"Unidade: {unidade_maior_faturamento}")
    print(f"Faturamento acumulado: R$ {valor_maior:,.2f}")
    
    return faturamento_acumulado

def pergunta_8(df):
    """
    Qual unidade apresenta o maior número de anomalias nos dados,
    considerando valores unitários fora do padrão e quantidades excessivamente altas?
    """
    print("\n" + "=" * 80)
    print("PERGUNTA 8: Unidade com mais anomalias")
    print("=" * 80)
    
    # Definir anomalias usando quartis
    Q1_valor = df['Valor Unitário'].quantile(0.25)
    Q3_valor = df['Valor Unitário'].quantile(0.75)
    IQR_valor = Q3_valor - Q1_valor
    limite_inf_valor = Q1_valor - 1.5 * IQR_valor
    limite_sup_valor = Q3_valor + 1.5 * IQR_valor
    
    Q1_qtd = df['Qtd'].quantile(0.25)
    Q3_qtd = df['Qtd'].quantile(0.75)
    IQR_qtd = Q3_qtd - Q1_qtd
    limite_sup_qtd = Q3_qtd + 1.5 * IQR_qtd
    
    # Identificar anomalias
    anomalias_valor = (df['Valor Unitário'] < limite_inf_valor) | (df['Valor Unitário'] > limite_sup_valor)
    anomalias_qtd = df['Qtd'] > limite_sup_qtd
    
    df['Anomalia'] = anomalias_valor | anomalias_qtd
    
    # Contar anomalias por unidade
    anomalias_unidade = df.groupby('Unidade')['Anomalia'].sum().sort_values(ascending=False)
    
    print("Número de anomalias por unidade:")
    for unidade, count in anomalias_unidade.items():
        print(f"{unidade}: {count} anomalias")
    
    print(f"\nUnidade com mais anomalias: {anomalias_unidade.index[0]} ({anomalias_unidade.iloc[0]} anomalias)")
    
    return anomalias_unidade

def pergunta_9(df):
    """
    Gere uma matriz de correlação entre todas as variáveis numéricas
    e interprete os resultados.
    """
    print("\n" + "=" * 80)
    print("PERGUNTA 9: Matriz de correlação")
    print("=" * 80)
    
    # Selecionar apenas variáveis numéricas
    df_numeric = df.select_dtypes(include=[np.number])
    
    # Calcular matriz de correlação
    correlacao = df_numeric.corr()
    
    print("Matriz de correlação:")
    print(correlacao.round(3))
    
    # Identificar correlações mais fortes (excluindo diagonal)
    correlacoes_fortes = []
    for i in range(len(correlacao.columns)):
        for j in range(i+1, len(correlacao.columns)):
            corr_value = correlacao.iloc[i, j]
            if abs(corr_value) > 0.5:  # Correlação moderada a forte
                correlacoes_fortes.append({
                    'Variavel_1': correlacao.columns[i],
                    'Variavel_2': correlacao.columns[j],
                    'Correlacao': corr_value
                })
    
    if correlacoes_fortes:
        print("\nCorrelações mais significativas (|r| > 0.5):")
        for corr in correlacoes_fortes:
            print(f"{corr['Variavel_1']} vs {corr['Variavel_2']}: {corr['Correlacao']:.3f}")
    
    return correlacao

def pergunta_10(df):
    """
    Considerando o desvio padrão dos valores de venda para cada vendedor,
    qual Cod_vendedor apresenta a maior consistência nas vendas
    (menor desvio padrão), desde que tenha realizado pelo menos 5 vendas?
    """
    print("\n" + "=" * 80)
    print("PERGUNTA 10: Vendedor com maior consistência")
    print("=" * 80)
    
    # Calcular estatísticas por vendedor
    stats_vendedor = df.groupby('Cod_vendedor').agg({
        'Valor Total': ['count', 'std', 'mean']
    }).round(2)
    
    stats_vendedor.columns = ['Num_Vendas', 'Desvio_Padrao', 'Media']
    stats_vendedor = stats_vendedor.reset_index()
    
    # Filtrar vendedores com pelo menos 5 vendas
    vendedores_filtrados = stats_vendedor[stats_vendedor['Num_Vendas'] >= 5]
    
    if len(vendedores_filtrados) > 0:
        vendedor_consistente = vendedores_filtrados.loc[vendedores_filtrados['Desvio_Padrao'].idxmin()]
        
        print(f"Vendedor mais consistente:")
        print(f"Código: {vendedor_consistente['Cod_vendedor']}")
        print(f"Desvio Padrão: R$ {vendedor_consistente['Desvio_Padrao']:,.2f}")
        print(f"Média de Vendas: R$ {vendedor_consistente['Media']:,.2f}")
        print(f"Número de Vendas: {vendedor_consistente['Num_Vendas']}")
    else:
        print("Nenhum vendedor atende ao critério de pelo menos 5 vendas")
    
    return vendedores_filtrados

def main():
    """Função principal que executa todas as análises."""
    print("ANÁLISE DE DADOS - LOJA BEMOL")
    print("=" * 80)
    
    # Carregar dados
    df = carregar_dados()
    
    print(f"Base de dados carregada: {len(df)} registros")
    print(f"Período: {df['Data_compra'].min().strftime('%Y-%m-%d')} a {df['Data_compra'].max().strftime('%Y-%m-%d')}")
    
    # Executar todas as perguntas
    pergunta_1(df)
    pergunta_2(df)
    pergunta_3(df)
    pergunta_4(df)
    pergunta_5(df)
    pergunta_6(df)
    pergunta_7(df)
    pergunta_8(df)
    pergunta_9(df)
    pergunta_10(df)
    
    print("\n" + "=" * 80)
    print("ANÁLISE CONCLUÍDA")
    print("=" * 80)

if __name__ == "__main__":
    main()