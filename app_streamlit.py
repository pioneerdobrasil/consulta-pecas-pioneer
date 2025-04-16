
import streamlit as st
import pandas as pd

st.set_page_config(layout="wide")

# Logo (carregando diretamente do GitHub)
st.image("https://raw.githubusercontent.com/pioneerdobrasil/consulta-pecas-pioneer/main/logo.png", width=180)

# Título
st.markdown("<h1 style='text-align: center; margin-top: -20px;'>Consulta de Peças e Modelos - Pioneer</h1>", unsafe_allow_html=True)

# Upload do Excel (oculto)
@st.cache_data
def carregar_dados():
    return pd.read_excel("Referência_Cruzada_2_Atualizada.xlsx")

df = carregar_dados()

# Layout lateral
st.sidebar.subheader("📑 Colunas detectadas:")
for coluna in df.columns:
    st.sidebar.markdown(f"- {coluna}")

# Interface de busca
col1, col2 = st.columns([1, 1])
coluna_busca = col1.selectbox("Buscar por:", df.columns)
tipo_busca = col2.selectbox("Tipo de busca:", ["Contém", "Igual"])

valor_busca = st.text_input("Digite o código")

col3, col4 = st.columns([1, 1])
buscar = col3.button("🔍 Procurar")
limpar = col4.button("🧹 Limpar busca")

# Lógica de busca
resultado = pd.DataFrame()
if buscar:
    if tipo_busca == "Contém":
        resultado = df[df[coluna_busca].astype(str).str.contains(valor_busca, case=False, na=False)]
    elif tipo_busca == "Igual":
        resultado = df[df[coluna_busca].astype(str) == valor_busca]

# Exibe resultado
if not resultado.empty:
    st.success(f"{len(resultado)} resultado(s) encontrado(s).")
    st.dataframe(resultado, use_container_width=True)
elif buscar:
    st.warning("Nenhum resultado encontrado.")

# Botão para limpar busca
if limpar:
    st.rerun()
