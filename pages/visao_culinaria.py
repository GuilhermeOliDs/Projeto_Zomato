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

st.set_page_config( page_title='Visão Culinária', page_icon='🍽️', layout='wide' )

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

# -------------------------------------------------------------------------------------Criação_do_tipo_categoria_comida----------------------------------------------------------------------------------------------
def create_price_type(price_range):
    if price_range == 1:
        return "cheap"
    elif price_range == 2:
        return "normal"
    elif price_range == 3:
        return "expensive"
    else:
        return "gourmet"

# -------------------------------------------------------------------------------------Criação_dos_nomes_das_cores---------------------------------------------------------------------------------------------------
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

# -------------------------------------------------------------------------------------Renomear as colunas do DataFrame----------------------------------------------------------------------------------------------
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

# -------------------------------------------------------------------------------------Renomeando as colunas do DataFrame--------------------------------------------------------------------------------------------
df1.rename(columns={'restaurant_id': 'Quantidade de restaurantes'}, inplace=True)

df1.rename(columns={'city': 'Cidade'}, inplace=True)

df1.rename(columns={'votes': 'Quantidade de avaliações'}, inplace=True)

df1.rename(columns={'average_cost_for_two': 'Preço de prato para duas pessoas'}, inplace=True)

df1.rename(columns={'aggregate_rating': 'Classificação agregada'}, inplace=True)

df1.rename(columns={'restaurant_name': 'Nome dos restaurantes'}, inplace=True)
# -------------------------------------------------------------------------------------Criando_colunas---------------------------------------------------------------------------------------------------------------
df1['Países'] = df1.loc[:, 'country_code'].apply(lambda x: country_name(x))

df1['price_type'] = df1.loc[:, 'price_range'].apply(lambda x: create_price_type(x))

df1['color'] = df1.loc[:, 'rating_color'].apply(lambda x: color_name(x))

df1["Culinárias"] = df1.loc[:, "cuisines"].apply(lambda x: x.split(",")[0])

# -------------------------------------------------------------------------------------Variavel tipos culinários-----------------------------------------------------------------------------------------------------
tipos_culinarios = list (df1['Culinárias'].unique())

culinarias_sel = ['Home-made', 'BBQ', 'Japanese', 'Brazilian', 'Arabian', 'American', 'Italian']


# -------------------------------------------------------------------------------------Variavel países---------------------------------------------------------------------------------------------------------------
paises = ["India", "Australia", "Brazil", "Canada", "Indonesia", "New Zeland", "Philippines", "Qatar", "Singapure", "South Africa", "Sri Lanka", "Turkey", "United Arab Emirates", "England", "United States of America"]

paises_sel = ["Brazil", "England", "Qatar", "South Africa", "Canada", "Australia"]

# ========================================================================================================================================================================
# BARRA LATERAL
# ========================================================================================================================================================================

st.title('🍽️ **Visão Culinárias**')

st.sidebar.markdown('🍽️ **Culinária**')

st.sidebar.markdown( '''___''')

st.sidebar.markdown( '## Filtros' )

opcoes_paises = st.sidebar.multiselect('Escolha os países que deseja visualizar as informações.', paises, default= paises_sel)

st.sidebar.markdown( '''___''')

quantidade_restaurantes = st.sidebar.slider('Selecione a quantidade de restaurantes que deseja visualizar.', 1, 20, 10)

st.sidebar.markdown( '''___''')


opcoes_culinarias = st.sidebar.multiselect('Selecione o tipo de culinária que deseja visualizar.', tipos_culinarios, default=culinarias_sel)


st.sidebar.markdown( '''___''')


st.sidebar.markdown( '### Powered by Guilherme Oliveira' )
#Filtro dos Países
linhas_selecionadas_paises = df1['Países'].isin(opcoes_paises)
  

#Filtro das Culinárias
linhas_selecionadas_culinarias = df1['Culinárias'].isin(opcoes_culinarias)


df2 = df1.loc[linhas_selecionadas_paises & linhas_selecionadas_culinarias, :]

# ========================================================================================================================================================================
# LAYOUT NO Stremlit
# ========================================================================================================================================================================
with st.container():
    st.markdown('## Melhores restaurantes dos principais tipos culinários.')
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        melhores = df1[df1['Culinárias'] == 'Italian']
        
        fim = melhores.loc[:, ['Classificação agregada', 'Nome dos restaurantes']].groupby(['Nome dos restaurantes']).max().sort_values('Classificação agregada', ascending=False).reset_index()
        
        teste = fim.loc[1, ['Nome dos restaurantes', 'Classificação agregada']]
        
        col1.metric(label="Culinária italiana", value="4.9/5.0", delta='Restaurante Darshan')
    
# -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------    
    with col2:
        melhores = df1[df1['Culinárias'] == 'Japanese']
        
        fim = (melhores.loc[:, ['Classificação agregada', 'Nome dos restaurantes', 'Culinárias']]
        .groupby(['Nome dos restaurantes']).max().sort_values('Classificação agregada', ascending=False).reset_index())
        
        final = fim.loc[1, ['Nome dos restaurantes', 'Classificação agregada']]
        
        col2.metric(label='Culinária japonesa', value='4.9/5.0', delta='Restaurante Chotto Matte')

# -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------    
    with col3:
        melhores = df1[df1['Culinárias'] == 'Brazilian']
        
        fim = (melhores.loc[:, ['Classificação agregada', 'Nome dos restaurantes', 'Culinárias']]
                                                          .groupby(['Nome dos restaurantes']).max().sort_values('Classificação agregada', ascending=False).reset_index())
        
        final = fim.loc[1, ['Nome dos restaurantes', 'Classificação agregada']]
        
        col3.metric(label='Culinária brasileira', value='4.9/5.0', delta='Restaurante Texas de Brazil')
        
# -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    
    with col4:
        melhores = df1[df1['Culinárias'] == 'American']
        
        fim = (melhores.loc[:, ['Classificação agregada', 'Nome dos restaurantes', 'Culinárias']]
                                                          .groupby(['Nome dos restaurantes']).max().sort_values('Classificação agregada', ascending=False).reset_index())
        
        final = fim.loc[1, ['Nome dos restaurantes', 'Classificação agregada']]
        
        col4.metric(label='Culinária americana', value='4.9/5.0', delta='Restaurante Park Burguer')
        
# -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    with col5:
        melhores = df1[df1['Culinárias'] == 'Korean']
        
        fim = (melhores.loc[:, ['Classificação agregada', 'Nome dos restaurantes', 'Culinárias']]
                                                          .groupby(['Nome dos restaurantes']).max().sort_values('Classificação agregada', ascending=False).reset_index())
        
        final = fim.loc[1, ['Nome dos restaurantes', 'Classificação agregada']]
        
        col5.metric(label='Culinária coreana', value='4.7/5.0', delta='Restaurante Soban K-Town Grill')

# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- 
st.markdown( '''___''')

with st.container():
    st.markdown(f"<h2 style='text-align: center;'> Top {quantidade_restaurantes} restaurantes. </h2", unsafe_allow_html=True)
    
    cols = ['Quantidade de avaliações', 'Nome dos restaurantes', 'Países', 'Cidade', 'Culinárias', 'Preço de prato para duas pessoas', 'Classificação agregada']
    
    classificacao = df2[df2['Classificação agregada'] == 4.9]
    
    count = df2.loc[:, cols].groupby(cols).max().sort_values(['Classificação agregada', 'Quantidade de avaliações'], ascending = False).reset_index()
    
    fim = count.head(quantidade_restaurantes)
    
    st.dataframe(fim)


# -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
st.markdown( '''___''')

with st.container():
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"<h5 style='text-align: center;'> Top {quantidade_restaurantes} melhores tipos de culinárias. </h5", unsafe_allow_html=True)
        
        top = df1.groupby(['Culinárias'])[['Classificação agregada']].mean().sort_values('Classificação agregada', ascending=False).reset_index()
        
        top_fim = top.head(quantidade_restaurantes)
        
        fig = px.bar(top_fim, x= 'Culinárias', y='Classificação agregada', color='Culinárias', template= 'plotly_dark' )
        
        st.plotly_chart(fig, use_container_width=True)
        
    with col2:
        st.markdown(f"<h5 style='text-align: center;'> Top {quantidade_restaurantes} piores tipos de culinárias. </h5", unsafe_allow_html=True)
        
        top = df1.groupby(['Culinárias'])[['Classificação agregada']].mean().sort_values('Classificação agregada', ascending=True).reset_index()
        
        top_fim = top.head(quantidade_restaurantes)
        
        fig = px.bar(top_fim, x= 'Culinárias', y='Classificação agregada', color='Culinárias', template= 'plotly_dark' )
        
        st.plotly_chart(fig, use_container_width=True)
        