import pandas as pd 

df_vendas = pd.read_csv("bases/amazon.csv")

df_vendas = pd.DataFrame(df_vendas)
df_vendas
df_vendas = df_vendas.sample(n=15, random_state=1)
#Começo LLM

from langchain_openai import ChatOpenAI
from langchain_groq import ChatGroq
from openai import OpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers.string import StrOutputParser
from dotenv import load_dotenv, find_dotenv

_ = load_dotenv(find_dotenv())
input_variables=['text', 'text2'],
template = """
Estou trabalhando em uma base de dados e quero fazer uma limpeza de dados.
Tenha uma base porem a parte de categoria esta mal organizada,
queria que voce pegasse a categoria ja cadastrada e a descricao e adptasse para categorias melhores


A categoria está como
{text}

E quero que escolha a categoria deste item:
{text2}

Responda apenas com a categoria do produto em ingles, pois vou colocar na nova categoria, portanto sem respostas longas, apenas a categoria, exemplo 'TV','Mousepad','Cable', porém não tem especifico, como 'Ballpoint Pens', ou 'Fountain Pens', quero que coloque como 'Pens' apenas.
"""

#Coloca o prompt em um template 
prompt = PromptTemplate.from_template(template=template)

#Seleciona o modelo
#chat = ChatGroq(model="llama-3.1-8b-instant")
chat = ChatGroq(model="llama-3.1-70b-versatile")

# Conectar o prompt ao chat
chain = prompt | chat | StrOutputParser()
categorias = []
for index, row in df_vendas.iterrows():
    # Cria a entrada para o batch
    input_data = {
        'text': row['category'],
        'text2': row['product_name']
    }
    categorias.append(input_data)

# Processar as categorias em batch
batch_responses = chain.batch(categorias)

# Atualizar o DataFrame com as novas categorias
df_vendas['category'] = [response for response in batch_responses]


# Salvar o DataFrame atualizado em um novo CSV
df_vendas.to_csv("bases/financeiro.csv", index=False)