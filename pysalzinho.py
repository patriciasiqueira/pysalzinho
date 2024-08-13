import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
pd.options.display.float_format = '{:.2f}'.format    # pandas: para todos os números aparecerem com duas casas decimais
import geopandas as gp
import pysal as ps
import splot
import mapclassify as mc
from libpysal.weights import Queen
from libpysal import weights
from esda import Moran, Moran_Local, G_Local
from splot.esda import plot_moran, moran_scatterplot, lisa_cluster, plot_local_autocorrelation


st.header('Produção agrícola (ton) por município em 2018')

dados = pd.read_csv('https://raw.githubusercontent.com/patriciasiqueira/patriciasiqueira.github.io/master/arquivos/culturas-2018.csv', encoding='utf-8')
cod = pd.read_csv('https://raw.githubusercontent.com/patriciasiqueira/patriciasiqueira.github.io/master/arquivos/codigos-municipios.csv', encoding='utf8')
dados = dados.merge(cod)
dados = dados.loc[:, ['mun', 'nome_mun', 'sigla_uf', 'nome_regiao', 'nome_meso',
       'nome_micro', 'algodao', 'arroz', 'banana', 'cafe', 'cana',
       'feijao', 'fumo', 'laranja', 'mandioca', 'milho', 'soja', 'tomate']]
link = 'https://raw.githubusercontent.com/lincolnfrias/dados/master/br.json'
geodf = gp.read_file(link)
geodf.rename(columns={'CD_GEOCMU': 'mun'}, inplace=True)  # mudar nome da coluna com cód. para 'mun'
geodf['mun'] = geodf.mun.astype(int)  # transformar códigos em inteiros
br = pd.merge(geodf, dados, on='mun')  # mesclar o dataframe e o shapefile
br = br.drop('NM_MUNICIP', axis=1)

st.header('Culturas agrícolas selecionadas para 2018')

culturas = br.columns[7:]
nome_cultura = st.selectbox('Selecione uma cultura: ', culturas, index=4) # Default to California

df = br.query("nome_micro == 'Varginha'")
df = df.reset_index(drop=True)      # iniciar índices com 0 e tirar a coluna 'index'

w = Queen.from_dataframe(df, use_index=False)
w.transform = 'r'
y = df['soja'].values
moran = Moran(y, w)
st.write(moran.I, moran.p_sim)

st.write("Criado por Patrícia.")