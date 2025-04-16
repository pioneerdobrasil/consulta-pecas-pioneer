
import streamlit as st
import pandas as pd
import io

# ---------- CONFIGURAÇÕES DE PÁGINA ----------
st.set_page_config(page_title="Consulta Pioneer", page_icon="📦", layout="wide")

# ---------- LOGO ----------
col_logo, col_titulo = st.columns([1, 6])
with col_logo:
    st.image("logotipo_pioneer_pantone201C.png", use_container_width=True)
with col_titulo:
    st.markdown("## Consulta de Peças e Modelos - Pioneer")

# ---------- SESSION STATE ----------
if "entrada" not in st.session_state:
    st.session_state.entrada = ""
if "limpar" not in st.session_state:
    st.session_state.limpar = False
if "buscar" not in st.session_state:
    st.session_state.buscar = False

@st.cache_data(show_spinner=False)
def carregar_dados():
    df = pd.read_excel("Referência_Cruzada_2_Atualizada.xlsx")

    st.sidebar.subheader("🧪 Colunas detectadas:")
    for col in df.columns:
        st.sidebar.write("-", col)

    df.columns = df.columns.str.strip().str.lower()

    codigo_col = next((col for col in df.columns if "código" in col), None)
    modelo_col = next((col for col in df.columns if "modelo" in col), None)

    if not codigo_col or not modelo_col:
        st.error("As colunas 'Código' ou 'Modelo' não foram encontradas.")
        return pd.DataFrame(), None, None

    df[codigo_col] = df[codigo_col].astype(str).str.strip().str.upper()
    df[modelo_col] = df[modelo_col].astype(str).str.strip().str.upper()

    return df, codigo_col, modelo_col

df, codigo_col, modelo_col = carregar_dados()

if df.empty:
    st.stop()

# ---------- FILTROS ----------
col1, col2 = st.columns(2)
with col1:
    campo_opcao = st.selectbox("Buscar por:", ["Código", "Modelo"])
with col2:
    tipo_busca = st.selectbox("Tipo de busca:", ["Contém", "Começa com", "Igual"])

entrada = st.text_input(f"Digite o {campo_opcao.lower()}", value=st.session_state.entrada).strip().upper()

if not st.session_state.limpar:
    st.session_state.entrada = entrada

# ---------- BOTÕES ----------
bcol1, bcol2 = st.columns([1, 1])
with bcol1:
    if st.button("🔍 Procurar"):
        st.session_state.buscar = True
with bcol2:
    if st.button("🧹 Limpar busca"):
        st.session_state.entrada = ""
        st.session_state.buscar = False
        st.session_state.limpar = True
        st.rerun()

campo = codigo_col if campo_opcao == "Código" else modelo_col
resultado = pd.DataFrame()

if st.session_state.entrada and st.session_state.buscar and not st.session_state.limpar:
    if tipo_busca == "Contém":
        resultado = df[df[campo].str.contains(st.session_state.entrada, na=False)]
    elif tipo_busca == "Começa com":
        resultado = df[df[campo].str.startswith(st.session_state.entrada)]
    elif tipo_busca == "Igual":
        resultado = df[df[campo] == st.session_state.entrada]

if st.session_state.limpar:
    st.session_state.limpar = False

# ---------- RESULTADO ----------
if not resultado.empty:
    st.success(f"{len(resultado)} resultado(s) encontrado(s).")
    st.dataframe(resultado, use_container_width=True)
elif st.session_state.buscar and st.session_state.entrada:
    st.warning("Nenhum resultado encontrado.")
