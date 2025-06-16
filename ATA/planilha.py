import streamlit as st
import pandas as pd
import datetime
from PIL import Image
import plotly.express as px
import plotly.graph_objects as go


df = pd.read_csv("vai.csv")
st.set_page_config(layout="wide")
st.markdown('<style>div.block-container{padding-top:3rem;}</style>', unsafe_allow_html=True)
image = Image.open('sapy.png')

st.sidebar.title("Filtros")
classificaçao = st.sidebar.multiselect("Classificação", options=df['Classificação'].unique(), default=None)
especies = st.sidebar.multiselect("Espécie", options=df['Espécie'].unique(), default=None)
familias = st.sidebar.multiselect("Família", options=df['Família'].unique(), default=None)


filtro_class = df['Classificação'].isin(classificaçao) if classificaçao else pd.Series([True] * len(df))
filtro_familia = df['Família'].isin(familias) if familias else pd.Series([True] * len(df))
filtro_especie = df['Espécie'].isin(especies) if especies else pd.Series([True] * len(df))
df_filtrado = df[filtro_class & filtro_familia & filtro_especie]
st.sidebar.download_button(
    label="📥 Baixar dados filtrados",
    data=df_filtrado.to_csv(index=False).encode('utf-8'),
    file_name="dados_filtrados.csv",
    mime="text/csv"
)


col1,nha1,col2 = st.columns([0.1,0.1,0.7]) 
with col1:
     st.image(image,width=200)
     
 

html_title = """
    <style>
    .title-test {
    font-weight:bold;
    padding:5px;
    border-radius:6px
    text-shadow: 2px 2px 4px rgba(0, 0, 0.8, 0.7);
    text-align: center;
    }
    </style>
    <center><h1 class="title-test">Dashboard Interativo Planilha Área 4</h1></center>"""
with col2:
    st.markdown("<div style='border-left:2px solid #ccc; height:100%; margin-left:10px; padding-left:10px'>", unsafe_allow_html=True)
    st.markdown(html_title,unsafe_allow_html=True)
    st.sidebar.markdown("ℹ️ Use os filtros acima para explorar os dados de forma personalizada.")
    st.markdown("<hr style='border:2px solid #0D1B2A; margin-top:10px; margin-bottom:20px'>", unsafe_allow_html=True)
    st.markdown("""
    <nav style="background-color: #1B263B; padding: 10px 20px; border-radius: 8px;">
    <a style="color:white; margin-right:20px;" href="#graficos">Gráficos</a>
    <a style="color:white; margin-right:20px;" href="#tabela">Tabela</a>l
    </nav>
    """, unsafe_allow_html=True)
  
    
def mostrar_total(df, titulo="Total de indivíduos", cor="#00ccff"):
    total = len(df)
    st.markdown(f"""
        <div style='
            background-color: #111111;
            padding: 20px;
            border-radius: 12px;
            box-shadow: 2px 2px 12px rgba(0, 0, 0, 0.7);
            text-align: center;
            margin-top: 10px;
            width: 170px;
        '>
            <h4 style='margin-bottom: 5px; color: #cccccc;'>{titulo}</h4>
            <h2 style='margin-top: 0; color: {cor};'>{total}</h2>
        </div>
    """, unsafe_allow_html=True)
def mostrar_familias(df, titulo="Total de famílias", cor="#ffaa00"):
    total = df_filtrado["Família"].nunique()
    st.markdown(f"""
        <div style='
            background-color: #111111;
            padding: 20px;
            border-radius: 12px;
            box-shadow: 2px 2px 12px rgba(0, 0, 0, 0.7);
            text-align: center;
            margin-top: 10px;
            width: 170px;
        '>
            <h4 style='margin-bottom: 5px; color: #cccccc;'>{titulo}</h4>
            <h2 style='margin-top: 0; color: {cor};'>{total}</h2>
        </div>
    """, unsafe_allow_html=True)
def mostrar_especies(df, titulo="Total de espécies", cor="#FF1493"):
    total = df_filtrado['Espécie'].nunique()
    st.markdown(f"""
        <div style='
            background-color: #111111;
            padding: 20px;
            border-radius: 12px;
            box-shadow: 2px 2px 12px rgba(0, 0, 0, 0.7);
            text-align: center;
            margin-top: 10px;
            width: 170px;
        '>
            <h4 style='margin-bottom: 5px; color: #cccccc;'>{titulo}</h4>
            <h2 style='margin-top: 0; color: {cor};'>{total}</h2>
        </div>
    """, unsafe_allow_html=True)



col3, nha2, col4, col5 = st.columns([0.040,0.1,0.6,0.6])
with col3:
    mostrar_total(df)
    mostrar_familias(df)
    mostrar_especies(df)
    st.write("\n\n\n")  
    box_date = str(datetime.datetime.now().strftime("%d %B %Y"))
    st.write(f"Last updated by: \n {box_date}")
  
with nha2:
    st.markdown("<div style='border-left:2px solid #ccc; height:100%; margin-left:10px; padding-left:10px'>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
    



with col4:
    contagem_familias = df_filtrado["Família"].value_counts().reset_index()
    contagem_familias.columns = ["Família", "Quantidade"]
    

    fig_familias = px.pie(contagem_familias, names = "Família", values = "Quantidade", labels={"Quantidade": "Número de indivíduos"},
                  title = "Frequência - Famílias",
                  hover_data= ["Quantidade"], template = "plotly_dark", height=600)
    fig_familias.update_layout(plot_bgcolor='#0D1B2A',        # fundo do gráfico
    paper_bgcolor='#0D1B2A',      
    margin=dict(l=20, r=20, t=50, b=20), title_x=0.35,                   
    title_font=dict(size=24, color='white'),
    font=dict(color='white'),
    legend_bgcolor='#0D1B2A',     
    legend_bordercolor='white',
    legend_borderwidth=1)
    st.plotly_chart(fig_familias, use_container_width=True)
    st.write("\n\n\n")
    st.dataframe(df.style.set_table_styles(
    [{'selector': 'th, td', 'props': [('min-width', '500px')]}]
    ),height=450,)
    
   

with col5:
    contagem_especies = df_filtrado["Espécie"].value_counts().reset_index()
    contagem_especies.columns = ["Espécie", "Quantidade"]

    fig_especies = px.bar(contagem_especies, x = "Quantidade", y = "Espécie", labels={"Quantidade": "Número de indivíduos"},
                  title = "Frequencia - Espécies", orientation='h',
                  hover_data= ["Quantidade"], template = "gridon", height=600,)
    fig_especies.update_layout( plot_bgcolor='#0D1B2A',        # fundo do gráfico
    paper_bgcolor='#0D1B2A',      
    margin=dict(l=20, r=20, t=50, b=20), title_x=0.5,                   
    title_font=dict(size=24, color='white'),
    font=dict(color='white'),
    legend_bgcolor='#0D1B2A',     
    legend_bordercolor='white',
    legend_borderwidth=1)
    st.plotly_chart(fig_especies, use_container_width=True)
    
    
    contagem_class = df_filtrado["Classificação"].value_counts().reset_index()
    origem = contagem_class = df_filtrado['Classificação'].value_counts().reset_index()
    contagem_class.columns = ['Classificação', 'Quantidade']


    fig = px.bar(contagem_class, x='Classificação',y='Quantidade',
                 title='Frequência por Classificação',template='plotly_dark')
    fig.update_layout(plot_bgcolor='#0D1B2A',        # fundo do gráfico
    paper_bgcolor='#0D1B2A',      
    margin=dict(l=20, r=20, t=50, b=20), title_x=0.3,                   
    title_font=dict(size=24, color='white'),
    font=dict(color='white'),
    legend_bgcolor='#0D1B2A',     
    legend_bordercolor='white',
    legend_borderwidth=1)
    st.write("\n\n\n")
    st.plotly_chart(fig, use_container_width=True)
    


   



            
