
import streamlit as st
import pandas as pd

st.set_page_config(layout="wide")

# Logo e título
col1, col2 = st.columns([1, 10])
with col1:
    st.image("logo_pioneer_240px.png", width=120)
with col2:
    st.markdown("<h1 style='text-align: center;'>Consulta de Peças e Modelos - Pioneer</h1>", unsafe_allow_html=True)

# Inputs de busca
col3, col4 = st.columns(2)
with col3:
    campo_busca = st.selectbox("Buscar por:", ["Código", "Modelo"])
with col4:
    tipo_busca = st.selectbox("Tipo de busca:", ["Contém", "Igual"])

texto_busca = st.text_input("Digite o código")

col5, col6 = st.columns([1, 2])
buscar = col5.button("🔍 Procurar")
limpar = col6.button("🧹 Limpar busca")

# Carregamento da base
@st.cache_data
def carregar_dados():
    return pd.read_excel("Referência_Cruzada_2_Atualizada.xlsx")

df = carregar_dados()

# Lógica de busca
resultado = pd.DataFrame()
if buscar and texto_busca.strip() != "":
    if campo_busca == "Código":
        if tipo_busca == "Contém":
            resultado = df[df["Código"].astype(str).str.contains(texto_busca, case=False, na=False)]
        else:
            resultado = df[df["Código"].astype(str).str.lower() == texto_busca.lower()]
    else:
        if tipo_busca == "Contém":
            resultado = df[df["Modelo"].astype(str).str.contains(texto_busca, case=False, na=False)]
        else:
            resultado = df[df["Modelo"].astype(str).str.lower() == texto_busca.lower()]

if limpar:
    st.experimental_set_query_params()
    st.rerun()

# Exibição da tabela
if not resultado.empty:
    st.success(f"{len(resultado)} resultado(s) encontrado(s).")
    st.dataframe(resultado, use_container_width=True)
