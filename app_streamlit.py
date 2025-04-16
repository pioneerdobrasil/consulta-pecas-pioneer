
import streamlit as st
import pandas as pd

st.set_page_config(layout="wide")

# Logo e título centralizados
col1, col2, col3 = st.columns([1, 5, 1])
with col1:
    st.image("logo_pioneer_240px.png", width=180)
with col2:
    st.markdown("<h1 style='text-align: center;'>Consulta de Peças e Modelos - Pioneer</h1>", unsafe_allow_html=True)

# Inicializa estado de busca
if "resultados" not in st.session_state:
    st.session_state.resultados = pd.DataFrame()
if "colunas" not in st.session_state:
    st.session_state.colunas = []

# Upload e recarregamento do banco de dados
@st.cache_data
def carregar_dados():
    return pd.read_excel("Referência_Cruzada_2_Atualizada.xlsx")

df = carregar_dados()
st.session_state.colunas = df.columns.tolist()

# Interface de busca
st.sidebar.markdown("### 📑 Colunas detectadas:")
for c in st.session_state.colunas:
    st.sidebar.markdown(f"- {c}")

tipo_busca = st.selectbox("Buscar por:", options=df.columns)
modo_busca = st.selectbox("Tipo de busca:", options=["Igual", "Contém"])
entrada = st.text_input("Digite o código")

col1, col2 = st.columns([1, 1])
with col1:
    if st.button("🔍 Procurar"):
        if entrada:
            if modo_busca == "Contém":
                resultados = df[df[tipo_busca].astype(str).str.contains(entrada, case=False, na=False)]
            else:
                resultados = df[df[tipo_busca].astype(str).str.lower() == entrada.lower()]
            st.session_state.resultados = resultados
with col2:
    if st.button("🧹 Limpar busca"):
        st.session_state.resultados = pd.DataFrame()
        st.experimental_rerun()

# Exibição
if not st.session_state.resultados.empty:
    st.success(f"{len(st.session_state.resultados)} resultado(s) encontrado(s).")
    st.dataframe(st.session_state.resultados, use_container_width=True)
    st.download_button("📄 Baixar CSV", st.session_state.resultados.to_csv(index=False), "resultado.csv", "text/csv")
    st.download_button("📊 Baixar Excel", st.session_state.resultados.to_excel(index=False, engine="openpyxl"), "resultado.xlsx", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
