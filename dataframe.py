import pandas as pd
import urllib.request
import numpy as np
import random

def df(url):
    response = urllib.request.urlopen(url)
    return pd.read_csv(response)

# Carregar os dados
github_csv_url = 'https://raw.githubusercontent.com/TabathaLarissa/TesteUpload/main/Mock_Data.csv'
df = df(github_csv_url)
df['Qtd repo estoque'] = (df['FORECAST 60D'] - df['STOCK'] + df['BREAK'])
df['Ruptura'] = (df['BREAK'] / df['SALE'])

random.seed(55)

dates = pd.date_range(start='2023-01-01', end='2023-06-01', freq='MS')
categories = ['Eletrônicos', 'Celular', 'Linha branca', 'Móveis']
regiao = ['Norte', 'Sul', 'Sudeste', 'Centro-Oeste', 'Nordeste']
criticidade = ['Baixa', 'Média', 'Alta']
uf = ['AC', 'AL', 'AP', 'AM', 'BA', 'CE', 'DF', 'ES', 'GO', 'MA', 'MT', 'MS', 'MG', 'PA', 'PB', 'PR', 'PE', 'PI', 'RJ', 'RN', 'RO', 'RS', 'RR', 'SC', 'SE', 'SP', 'TO'] 

n = len(dates) * (100 // len(dates))

df = pd.DataFrame()

df['DATE'] = np.tile(dates, 100 // len(dates))
df['SKU'] = [f'{i}' for i in range(1, n + 1)]
df['CATEGORY'] = [random.choice(categories) for _ in range(n)]
df['UF'] = [random.choice(uf) for _ in range(n)]
df['CRITICIDADE'] = [random.choice(criticidade) for _ in range(n)]
df['REGIAO'] = [random.choice(regiao) for _ in range(n)]
df['SALE'] = [random.randint(1, 300) for _ in range(n)]
df['FORECAST 15D'] = [random.randint(1, 600) for _ in range(n)]
df['FORECAST 30D'] = [random.randint(1, 600) for _ in range(n)]
df['FORECAST 60D'] = [random.randint(1, 800) for _ in range(n)]
df['STOCK'] = [random.randint(1, 1000) for _ in range(n)]
df['BREAK'] =  df['SALE']/df['STOCK']
df['Qtd repo estoque'] = (df['FORECAST 60D'] - df['STOCK'] + df['BREAK'])
df['Ruptura'] = df['SALE']/df['STOCK']