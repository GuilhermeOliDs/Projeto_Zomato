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

st.set_page_config( page_title='Visão Cidade', page_icon='🏙️', layout='wide' )

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

# -------------------------------------------------------------------------------------Renomeando as colunas do DataFrame----------------------------------------------
df1.rename(columns={'restaurant_id': 'Quantidade de restaurantes'}, inplace=True)

df1.rename(columns={'city': 'Cidade'}, inplace=True)

df1.rename(columns={'votes': 'Quantidade de avaliações'}, inplace=True)

df1.rename(columns={'average_cost_for_two': 'Preço de prato para duas pessoas'}, inplace=True)

df1.rename(columns={'aggregate_rating': 'Classificação agregada'}, inplace=True)
# -------------------------------------------------------------------------------------Criando_colunas----------------------------------------------
df1['Países'] = df1.loc[:, 'country_code'].apply(lambda x: country_name(x))

df1['price_type'] = df1.loc[:, 'price_range'].apply(lambda x: create_price_type(x))

df1['color'] = df1.loc[:, 'rating_color'].apply(lambda x: color_name(x))

df1["Quantidade de tipos culinários"] = df1.loc[:, "cuisines"].apply(lambda x: x.split(",")[0])

# ========================================================================================================================================================================
# BARRA LATERAL
# ========================================================================================================================================================================

st.title('🏙️ **Visão Cidades**')

st.sidebar.markdown('🏙️ **Cidades**')

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
    st.markdown("<h6 style='text-align: center;'> Top 10 cidades com mais restaurantes na base de dados</h6", unsafe_allow_html=True)
    
    result = df1.groupby(['Cidade', 'Países'])[['Quantidade de restaurantes']].count().sort_values('Quantidade de restaurantes', ascending= False).reset_index()

    perfect = result.head(10)
    
    interacao1 = perfect[perfect['Países'].isin(opcoes_paises)]
    
    fig  =  px.bar( perfect ,  x = 'Cidade' ,  y = 'Quantidade de restaurantes', color='Países', template= 'plotly_dark' )  
    
    st.plotly_chart(fig, use_container_width=True)
    
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------
with st.container():
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("<h6 style='text-align: center;'> Top 7 cidades com restaurantes com média de avaliação acima de 4</h6", unsafe_allow_html=True)
        
        linhas = df1[df1['Classificação agregada'] >= 4]

        selecao = linhas.groupby(['Cidade', 'Países']).count().sort_values('Classificação agregada', ascending=False).reset_index()

        fim = selecao.head(7)
        
        interacao2 = fim[fim['Países'].isin(opcoes_paises)]
        
        fig = px.bar(fim, x= 'Cidade', y='Quantidade de restaurantes', color='Países', template= 'plotly_dark' )
        
        st.plotly_chart(fig, use_container_width=True)
        
        
    with col2:
        st.markdown("<h6 style='text-align: center;'> Top 7 cidades com restaurantes com média de avaliação abaixo de 2.5</h6", unsafe_allow_html=True)

        linhas = df1[df1['Classificação agregada'] <= 2.5]

        selecao = linhas.groupby(['Cidade', 'Países']).count().sort_values('Classificação agregada', ascending=False).reset_index()

        loc = selecao.head(7)
        
        interacao3 = loc[loc['Países'].isin(opcoes_paises)]
        
        fig = px.bar(loc, x= 'Cidade', y='Quantidade de restaurantes', color='Países', template= 'plotly_dark' )
        
        st.plotly_chart(fig, use_container_width=True)
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------
with st.container():
    st.markdown("<h6 style='text-align: center;'> Top 10 cidades com mais restaurantes com tipos culinários distintos</h6", unsafe_allow_html=True)
    
    linhas_sel = df1.loc[df1['Quantidade de tipos culinários'] != 'Quantidade de tipos culinários', :]
    
    linhas_sel1 = linhas_sel.loc[:, ['Cidade', 'Quantidade de tipos culinários', 'Países']].groupby(['Cidade', 'Países']).nunique().sort_values('Quantidade de tipos culinários', ascending = False).reset_index()
    
    top = linhas_sel1.head(10)
    
    interacao4 = top[top['Países'].isin(opcoes_paises)]
    
    fig = px.bar(top, x= 'Cidade', y='Quantidade de tipos culinários', color='Países', template= 'plotly_dark' )
    
    st.plotly_chart(fig, use_container_width=True)