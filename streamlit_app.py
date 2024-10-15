import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide")

st.title("🎈 Dashboard produtos amazon")
st.write(
    "Projetinho com tratamento feito com pandas e categorizado com IA e depois feito um dash em streamlit."
)

# Carregar os dados
df = pd.read_csv("bases/financeiro.csv")

# Limpar a coluna 'actual_price'
df['actual_price'] = df['actual_price'].replace({'₹': '', ',': ''}, regex=True).astype(float)

# Função para filtrar dados
def filter_data(df, selected_categories, price_range):
    df_filtered = df.copy()
    if selected_categories:
        df_filtered = df_filtered[df_filtered['category'].isin(selected_categories)]
    # Filtrar pela faixa de preço
    df_filtered = df_filtered[(df_filtered['actual_price'] >= price_range[0]) & (df_filtered['actual_price'] <= price_range[1])]
    return df_filtered

# Filtros de data
st.sidebar.header("Filtros")

# Filtro de categoria
categories = df["category"].unique().tolist()
selected_categories = st.sidebar.multiselect("Filtrar por Categorias", categories, default=categories)

# Filtro de faixa de preço
min_price = df["actual_price"].min()
max_price = df["actual_price"].max()
price_range = st.sidebar.slider("Filtrar por Faixa de Preço", min_value=float(min_price), max_value=float(max_price), value=(float(min_price), float(max_price)))

# Filtrar dados com base na seleção
df_filtered = filter_data(df, selected_categories, price_range)

# ====================
# Abas do dashboard
page = st.sidebar.radio("Selecione a Página", ("Visão Geral", "Relatórios"))

if page == "Visão Geral":
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

elif page == "Relatórios":
    st.subheader("Relatórios de Produtos")

    # Produtos mais rentáveis
    st.write("### Produtos Mais Rentáveis")
    top_products = df_filtered.groupby(['product_name'])['actual_price'].sum().reset_index()
    top_products = top_products.sort_values(by='actual_price', ascending=False).head(10)  # Top 10
    st.dataframe(top_products)

    # Categorias em alta
    st.write("### Categorias em Alta")
    category_performance = df_filtered['category'].value_counts().reset_index()
    category_performance.columns = ['category', 'product_count']
    top_categories = category_performance.sort_values(by='product_count', ascending=False).head(10)  # Top 10
    st.dataframe(top_categories)

    st.write("### Produtos Menos Rentáveis")
    top_products = df_filtered.groupby(['product_name'])['actual_price'].sum().reset_index()
    top_products = top_products.sort_values(by='actual_price', ascending=True).head(10)  # Top 10
    st.dataframe(top_products)
