
import streamlit as st
import pandas as pd
import unicodedata

# Configuração da página
st.set_page_config(layout="centered", page_title="Consulta de Peças e Modelos - Pioneer")

# Logo e título
col1, col2 = st.columns([1, 8])
with col1:
    st.image("logo.png", width=160)
with col2:
    st.markdown("<h1 style='text-align: center;'>Consulta de Peças e Modelos - Pioneer</h1>", unsafe_allow_html=True)

# Função para remover acentos
def remover_acentos(txt):
    if isinstance(txt, str):
        return unicodedata.normalize('NFKD', txt).encode('ASCII', 'ignore').decode('utf-8')
    return txt

# Carregamento do banco de dados
@st.cache_data
def carregar_dados():
    df = pd.read_excel("Referência_Cruzada_2_Atualizada.xlsx")
    df.columns = df.columns.str.lower()
    df = df.applymap(remover_acentos)
    return df

df = carregar_dados()

# Interface de busca
col1, col2 = st.columns(2)
criterio = col1.selectbox("Buscar por:", ["Modelo", "Código", "Descrição", "Depósito", "Categoria"])
tipo_busca = col2.selectbox("Tipo de busca:", ["Contém", "Igual"])

texto_busca = st.text_input("Digite o código")

col1, col2 = st.columns([1, 2])
buscar = col1.button("🔍 Procurar")
limpar = col2.button("🖉 Limpar busca")

if limpar:
    st.rerun()

if buscar and texto_busca:
    texto_busca = remover_acentos(texto_busca).lower()
    if tipo_busca == "Contém":
        resultado = df[df[criterio.lower()].astype(str).str.lower().str.contains(texto_busca)]
    elif tipo_busca == "Igual":
        resultado = df[df[criterio.lower()].astype(str).str.lower() == texto_busca]
    
    st.success(f"{len(resultado)} resultado(s) encontrado(s).")
    st.dataframe(resultado, use_container_width=True)
