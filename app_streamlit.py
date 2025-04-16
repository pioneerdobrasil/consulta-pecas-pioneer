
import streamlit as st
import pandas as pd

st.set_page_config(layout="wide")

@st.cache_data
def carregar_dados():
    return pd.read_excel("Referência_Cruzada_2_Atualizada.xlsx")

def buscar_dados(df, coluna, termo, tipo_busca):
    if tipo_busca == "Contém":
        return df[df[coluna].astype(str).str.contains(termo, case=False, na=False)]
    elif tipo_busca == "Igual":
        return df[df[coluna].astype(str).str.lower() == termo.lower()]
    elif tipo_busca == "Começa com":
        return df[df[coluna].astype(str).str.lower().str.startswith(termo.lower())]
    elif tipo_busca == "Termina com":
        return df[df[coluna].astype(str).str.lower().str.endswith(termo.lower())]
    return df

st.markdown(
    """<div style='text-align: center;'>
        <img src='https://upload.wikimedia.org/wikipedia/commons/2/22/Pioneer_logo_pantone201C.png' width='180'/>
        <h2 style='margin-top: 5px;'>Consulta de Peças e Modelos - Pioneer</h2>
    </div>""",
    unsafe_allow_html=True
)

df = carregar_dados()

with st.sidebar:
    st.markdown("### 🧾 Colunas detectadas:")
    for col in df.columns:
        st.markdown(f"- {col}")

col1, col2 = st.columns([2, 2])
with col1:
    campo_busca = st.selectbox("Buscar por:", df.columns.tolist(), index=0)
with col2:
    tipo_busca = st.selectbox("Tipo de busca:", ["Contém", "Igual", "Começa com", "Termina com"])

coluna_texto = st.text_input("Digite o código", key="input_busca")
col3, col4 = st.columns([1, 1])

resultado = pd.DataFrame()

with col3:
    if st.button("🔍 Procurar"):
        resultado = buscar_dados(df, campo_busca, coluna_texto, tipo_busca)

with col4:
    if st.button("🧹 Limpar busca"):
        st.session_state.input_busca = ""
        resultado = pd.DataFrame()

if not resultado.empty:
    st.success(f"{len(resultado)} resultado(s) encontrado(s).")
    st.dataframe(resultado, use_container_width=True)
    col5, col6 = st.columns([1, 1])
    with col5:
        csv = resultado.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Baixar CSV", csv, "resultado.csv", "text/csv", use_container_width=True)
    with col6:
        excel_bytes = resultado.to_excel(index=False, engine='openpyxl')
        st.download_button("📥 Baixar Excel", excel_bytes, "resultado.xlsx", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", use_container_width=True)
