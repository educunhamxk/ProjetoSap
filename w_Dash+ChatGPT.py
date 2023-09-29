import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px
import urllib.request
import requests
import openai
import os

# URL do arquivo CSV público no GitHub (substitua pela URL do seu arquivo)
github_csv_url = 'https://raw.githubusercontent.com/TabathaLarissa/TesteUpload/main/Mock_Data.csv'

# Baixar o arquivo CSV
responsed = urllib.request.urlopen(github_csv_url)

# Ler o CSV usando o pandas
df = pd.read_csv(responsed)

st.title('Stock ON')
    
total_sale = df['SALE'].sum()
total_stock = df['STOCK'].sum()
total_break = df['BREAK'].sum()

st.write('<h2 style="text-align: center;">Totais</h2>', unsafe_allow_html=True)
col1, col2, col3 = st.columns(3)
with col1:
    st.info('Total de Vendas (SALE)')
    st.text(total_sale)
with col2:
    st.info('Total de Estoque (STOCK)')
    st.text(total_stock)
with col3:
    st.info('Total de Quebras (BREAK)')
    st.text(total_break)

openai.api_key = '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'

response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "user", "content": f'O dataset a seguir corresponde à métricas de gestão de estoque, ruptura, venda e previsão de demanda. Me informe 5 insights sobre este dataset {df}'},
    ]
)
st.markdown(response['choices'][0]['message']['content'])