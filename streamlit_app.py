import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide", page_title='Dashboard Amazon Products')

st.title("🎈 Dashboard produtos Amazon")
st.write(
    "Projetinho com tratamento feito com pandas e categorizado com IA e depois feito um dash em streamlit."
)

# Carregar os dados
df = pd.read_csv("bases/financeiro.csv")

# Limpar a coluna 'actual_price'
df['actual_price'] = df['actual_price'].replace({'₹': '', ',': ''}, regex=True).astype(float)


def filter_data(df, selected_categories):
    df_filtered = df.copy()  # Inicializa df_filtered com o DataFrame original
    if selected_categories:
        df_filtered = df_filtered[df_filtered['category'].isin(selected_categories)]  # Filtra o DataFrame
    return df_filtered

# Filtros de data
st.sidebar.header("Filtros")

# Filtro de categoria
categories = df["category"].unique().tolist()
selected_categories = st.sidebar.multiselect("Filtrar por Categorias", categories, default=categories)

# Filtrar dados com base na seleção
df_filtered = filter_data(df, selected_categories)

# ====================
c1, c2 = st.columns([0.6, 0.4])

# Mostrar tabela filtrada
c1.subheader("Tabela de Finanças Filtradas")
c1.dataframe(df_filtered)

c2.subheader("Distribuição de Categorias")

# Verifica se df_filtered não está vazio
if not df_filtered.empty:
    # Remover duplicatas para considerar apenas preços únicos
    unique_prices = df_filtered.drop_duplicates(subset=['category', 'actual_price'])
    
    # Agregação para soma de preços únicos
    price_distribution = unique_prices.groupby("category")["actual_price"].sum().reset_index()
    price_distribution.columns = ['category', 'total_price']  # Renomear para melhor clareza
    price_distribution

    # Gráfico para soma dos preços únicos
    fig_price = px.pie(price_distribution, values='total_price', names='category',
                        title='Soma dos Preços Únicos por Categoria', hole=0.3)
    c2.plotly_chart(fig_price, use_container_width=True)

    # Agregação para quantidade de produtos
    quantity_distribution = df_filtered['category'].value_counts().reset_index()
    quantity_distribution.columns = ['category', 'product_count']  # Renomear para melhor clareza

    # Gráfico para quantidade de produtos
    fig_quantity = px.bar(quantity_distribution, x='category', y='product_count',
                           title='Quantidade de Produtos por Categoria')
    c2.plotly_chart(fig_quantity, use_container_width=True)

else:
    c2.write("Nenhum dado disponível após o filtro.")