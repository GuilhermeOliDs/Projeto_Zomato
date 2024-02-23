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
from folium.plugins import MarkerCluster
import numpy as np
from folium.plugins import FastMarkerCluster
# -------------------------------------------------------------------------------------Layout superior-------------------------------------------

st.set_page_config( page_title='Página inicial', page_icon='⚙️', layout='wide' )

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

image = Image.open( 'logo.png' )
st.sidebar.image( image, width=300 )

st.sidebar.markdown('# **Fome zero**')

st.sidebar.markdown( '''___''')

st.sidebar.markdown( '## Filtros' )

st.sidebar.markdown( 'Escolha os países que deseja visualizar as informações' )

opcoes_paises = st.sidebar.multiselect('Escolha uma opção', ["India", "Australia", "Brazil", "Canada", "Indonesia", "New Zeland", "Philippines", "Qatar", "Singapure", "South Africa", "Sri Lanka",
                                                             "Turkey", "United Arab Emirates", "England", "United States of America"], default= ["Brazil", "England", "Qatar", "South Africa", "Canada", 
                                                                                                                                                 "Australia"])

st.sidebar.markdown( '### Powered by Guilherme Oliveira' )
# -------------------------------------------------------------------------------------Condição de países----------------------------------------------

linhas_selecionadas = df1['Países'].isin(opcoes_paises)
df1 = df1.loc[linhas_selecionadas, :]

# ========================================================================================================================================================================
# LAYOUT NO Stremlit
# ========================================================================================================================================================================
with st.container():
    col1, col2, col3, col4, col5 = st.columns(5)
    
    st.markdown("<h1 style='text-align: center;'>Fome zero!</h1", unsafe_allow_html=True)
    
    st.markdown( '''___''')

    st.markdown("<h3 style='text-align: center;'> O melhor lugar para encontrar seu mais novo restaurante favorito!</h3", unsafe_allow_html=True)
    
    st.markdown("<h4 style='text-align: center;'> Temos as seguintes marcas dentro da nossa plataforma:</h4", unsafe_allow_html=True)
    
    st.markdown( '''___''')
    
    
with st.container():
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.markdown('**Restaurantes cadastrados:** ')
        st.header(':green[6929] ')
        
    with col2:
        st.markdown('**Países cadastrados:** ')
        st.header('  :green[15] ')
        
        
    with col3:
        st.markdown('**Cidades cadastradas:** ')
        st.header(':green[125]')

        
    with col4:
        st.markdown('**Avaliações feitas na plataforma:**')
        st.header(':green[4.194.533]')
        
    
    with col5:
        st.markdown('**Tipos de culinárias oferecidas:**')
        st.header(':green[165]')
        
st.markdown( '''___''')
# -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
st.container()
st.write ('### 🌎 Mapa com a Localização dos restaurantes')

df_aux = (df1.loc[:, ['Cidade', 'Classificação agregada', 'currency', 'Quantidade de tipos culinários', 'color', 'Quantidade de restaurantes','latitude', 'longitude', 'Preço de prato para duas pessoas', 'restaurant_name']]
         .groupby(['Cidade', 'Quantidade de tipos culinários','color', 'currency', 'Quantidade de restaurantes', 'restaurant_name'])
         .median().reset_index())


map1 = folium.Map()
marker_cluster = folium.plugins.MarkerCluster().add_to(map1)

                    
for i in range ( len (df_aux) ):
    popup_html = f'<div style="width: 250px;">' \
                 f"<b>{df_aux.loc[i, 'restaurant_name']}</b><br><br>" \
                 \
                 f"Preço para dois: {df_aux.loc[i, 'Preço de prato para duas pessoas']:.2f} ( {df_aux.loc[i, 'currency']})<br> " \
                 f"Type: {df_aux.loc[i, 'Quantidade de tipos culinários']}<br>" \
                 f"Nota: {df_aux.loc[i, 'Classificação agregada']}/5.0" \
                 f'</div>'
    folium.Marker ([df_aux.loc[i, 'latitude'], df_aux.loc[i, 'longitude']],
                   popup=popup_html, width=500, height=500, tooltip='clique aqui', parse_html=True,  
                   zoom_start=30, tiles= 'Stamen Toner', 
                   icon=folium.Icon(color=df_aux.loc[i, 'color'] , icon='home')).add_to(marker_cluster)
    
folium_static(map1, width=1200 , height=600 )
    
    
    