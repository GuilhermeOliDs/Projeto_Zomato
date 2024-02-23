# -------------------------------------------------------------------------------------Bibliotecas---------------------------------------------------
import inflection
from haversine import haversine
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
import datetime
from PIL import Image
import folium
from streamlit_folium import folium_static
import pandas as pd

# -------------------------------------------------------------------------------------Layout superior-------------------------------------------

st.set_page_config( page_title='Visão País', page_icon='🌍', layout='wide' )

# -------------------------------------------------------------------------------------Importando_Dataframe-------------------------------------------
df = pd.read_csv('dataset/zomato.csv')

# -------------------------------------------------------------------------------------Fazendo_cópia_DF-----------------------------------------------
df1 = df.copy()

# -------------------------------------------------------------------------------------Limpeza_de_NA_e_Duplicatas----------------------------------------------
df1 = df1.dropna()
df1 = df1.drop_duplicates()

# -------------------------------------------------------------------------------------Preenchimento do nome dos países-----------------------------------------------
COUNTRIES = {
    1: "India",
    14: "Australia",
    30: "Brazil",
    37: "Canada",
    94: "Indonesia",
    148: "New Zeland",
    162: "Philippines",
    166: "Qatar",
    184: "Singapure",
    189: "South Africa",
    191: "Sri Lanka",
    208: "Turkey",
    214: "United Arab Emirates",
    215: "England",
    216: "United States of America",
}
def country_name(country_id):
    return COUNTRIES[country_id]

# -------------------------------------------------------------------------------------Criação_do_tipo_categoria_comida-----------------------------------------------
def create_price_type(price_range):
    if price_range == 1:
        return "cheap"
    elif price_range == 2:
        return "normal"
    elif price_range == 3:
        return "expensive"
    else:
        return "gourmet"

# -------------------------------------------------------------------------------------Criação_dos_nomes_das_cores----------------------------------------------
COLORS = {
    "3F7E00": "darkgreen",
    "5BA829": "green",
    "9ACD32": "lightgreen",
    "CDD614": "orange",
    "FFBA00": "red",
    "CBCBC8": "darkred",
    "FF7800": "darkred",
}
def color_name(color_code):
    return COLORS[color_code]

# -------------------------------------------------------------------------------------Renomear as colunas do DataFrame----------------------------------------------
def rename_columns(dataframe):
    df = dataframe.copy()
    title = lambda x: inflection.titleize(x)
    snakecase = lambda x: inflection.underscore(x)
    spaces = lambda x: x.replace(" ", "")
    cols_old = list(df.columns)
    cols_old = list(map(title, cols_old))
    cols_old = list(map(spaces, cols_old))
    cols_new = list(map(snakecase, cols_old))
    df.columns = cols_new
    return df
df1 = rename_columns(df1)

# -------------------------------------------------------------------------------------Renomeando as colunas DataFrame----------------------------------------------
df1.rename(columns={'restaurant_id': 'Quantidade de restaurantes'}, inplace=True)

df1.rename(columns={'city': 'Quantidade de cidades'}, inplace=True)

df1.rename(columns={'votes': 'Quantidade de avaliações'}, inplace=True)

df1.rename(columns={'average_cost_for_two': 'Preço de prato para duas pessoas'}, inplace=True)
# -------------------------------------------------------------------------------------Criando_colunas----------------------------------------------
df1['Países'] = df1.loc[:, 'country_code'].apply(lambda x: country_name(x))

df1['price_type'] = df1.loc[:, 'price_range'].apply(lambda x: create_price_type(x))

df1['color'] = df1.loc[:, 'rating_color'].apply(lambda x: color_name(x))

df1["cuisines"] = df1.loc[:, "cuisines"].apply(lambda x: x.split(",")[0])

# ========================================================================================================================================================================
# BARRA LATERAL
# ========================================================================================================================================================================

st.title(':earth_americas: **Visão Países**')

st.sidebar.markdown(':earth_americas: **Countries**')

st.sidebar.markdown( '''___''')

st.sidebar.markdown( '## Filtros' )

st.sidebar.markdown( 'Escolha os países que deseja visualizar as informações' )

opcoes_paises = st.sidebar.multiselect('Escolha uma opção', ["India", "Australia", "Brazil", "Canada", "Indonesia", "New Zeland", "Philippines", "Qatar", "Singapure", "South Africa", "Sri Lanka",
                                                             "Turkey", "United Arab Emirates", "England", "United States of America"], default= ["Brazil", "England", "Qatar", "South Africa", "Canada", 
                                                                                                                                                 "Australia"])


st.sidebar.markdown( '### Powered by Guilherme Oliveira' )
#========================================================================================================================================================================
# LAYOUT NO Stremlit
# ========================================================================================================================================================================
with st.container():
    st.markdown("<h6 style='text-align: center;'> Quantidade de restaurantes registrados por país</h6", unsafe_allow_html=True)
    
    country_rest1 = df1.loc[:, ['Países', 'Quantidade de restaurantes']].groupby('Países').count().sort_values('Quantidade de restaurantes', ascending = False ).reset_index()
    
    interação = country_rest1[country_rest1['Países'].isin(opcoes_paises)]
    
    fig = px.bar( interação, x='Países', y='Quantidade de restaurantes' )
    
    st.plotly_chart(fig, use_container_width=True )
    
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------
with st.container():
    st.markdown("<h6 style='text-align: center;'> Quantidade de cidades registradas por país</h6>", unsafe_allow_html=True)
    
    country_city = df1.loc[:, ['Países', 'Quantidade de cidades']].groupby(['Países','Quantidade de cidades']).count().reset_index()

    country_city1 = country_city.loc[:, ['Quantidade de cidades', 'Países']].groupby('Países').count().sort_values('Quantidade de cidades', ascending = False ).reset_index()
    
    interacao = country_city1[country_city1['Países'].isin(opcoes_paises)]
    
    fig = px.bar( interacao, x='Países', y='Quantidade de cidades' )
    
    st.plotly_chart(fig, use_container_width=True)
    
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------
with st.container():
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("<h6 style='text-align: center;'> Média de avaliação feitas por país</h6>", unsafe_allow_html=True)
        
        country_mean = round( df1.loc[:, ['Países', 'Quantidade de avaliações']].groupby('Países').mean().sort_values('Quantidade de avaliações', ascending = False).reset_index(), 2 )
        
        interação = country_mean[country_mean['Países'].isin(opcoes_paises)]
        
        fig = px.bar(interação, x='Países', y='Quantidade de avaliações' )
        
        st.plotly_chart(fig, use_container_width=True)
        
        
    with col2:
        st.markdown("<h6 style='text-align: center;'> Média de preço de um prato para duas pessoas por país</h6>", unsafe_allow_html=True)
        
        mean_ave_two = round( df1.loc[:, ['Países', 'Preço de prato para duas pessoas']].groupby('Países').mean().reset_index(), 2)
        
        interação = mean_ave_two[mean_ave_two['Países'].isin(opcoes_paises)]
        
        fig = px.bar(interação, x='Países', y='Preço de prato para duas pessoas')
        
        st.plotly_chart(fig, use_container_width=True)