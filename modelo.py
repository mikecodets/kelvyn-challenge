import pandas as pd
import matplotlib.pyplot as plt

# Simulando um DataFrame (caso não tenha um CSV)
data = {
    "Produto": ["Celular", "Notebook", "Tablet", "Celular", "Notebook", "Tablet"],
    "Categoria": ["Eletrônico", "Eletrônico", "Eletrônico", "Eletrônico", "Eletrônico", "Eletrônico"],
    "Valor": [1500, 3500, 1200, 1700, 4000, 1300]
}

# Criando um DataFrame
df = pd.DataFrame(data)

# Agrupando os dados por categoria e somando os valores
df_grouped = df.groupby("Produto")["Valor"].sum().reset_index()

# Criando o gráfico de barras
plt.figure(figsize=(8, 5))
plt.bar(df_grouped["Produto"], df_grouped["Valor"], color="royalblue")
plt.xlabel("Produto")
plt.ylabel("Total Vendido (R$)")
plt.title("Total de Vendas por Produto")
plt.grid(axis="y", linestyle="--", alpha=0.7)
plt.show()


'''
Gabarito:

1) Unidade:  10.1
   Unidade:  10.1
   Unidade:  10.1
   Unidade:  10.1
   Unidade:  10.1
   Unidade:  10.1
2) Unidade: 'xxxxx'
   Produto: 'xxxxx'
   Quantidade: xxxx
3) Vendedor: xxxxx
   Total: R$ xxxxx
4) Centro: xxxxx
   Categoria: xxxxx
   Valor Total: R$ xxxxx
5) Centro: xxxxx
   Valor do ticket médio: R$ xxxxx
6) Unidade: xxxxx
   Total de vendas: 10.1
   Categoria: xxxxx
   Produto: xxxxx
   Quantidade: 1
7) Centro: xxxxx
   Produto: xxxxx
   Valor: R$ xxxxx
   Segundo: xxxxx
   Valor total segundo colocado: R$ xxxxx
   Diferença percentual: 10.1%
8) Eletrodomésticos: 10.1%
   Eletroportáteis: 10.1%
   Informática: 10.1%
   Móveis: 10.1%
9) Nome
   Nome
   Nome
   Nome
   Nome
10) Unidade: 10.1
    Unidade: 10.1
    Unidade: 10.1
    Unidade: 10.1
    Unidade: 10.1
    Unidade: 10.1
        
'''