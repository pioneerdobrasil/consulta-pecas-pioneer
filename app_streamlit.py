
import streamlit as st
import pandas as pd
import json

# Função para autenticar usuários
def autenticar_usuario(usuario, senha):
    try:
        with open("usuarios.json", "r") as f:
            usuarios = json.load(f)
        return usuario in usuarios and usuarios[usuario] == senha
    except FileNotFoundError:
        return False

# Layout de login
if "autenticado" not in st.session_state:
    st.session_state.autenticado = False

if not st.session_state.autenticado:
    st.image("logo_pioneer_240px.png", width=120)
    st.title("Login")
    usuario = st.text_input("Usuário")
    senha = st.text_input("Senha", type="password")
    if st.button("Entrar"):
        if autenticar_usuario(usuario, senha):
            st.session_state.autenticado = True
            st.experimental_rerun()
        else:
            st.error("Usuário ou senha incorretos.")
    st.stop()

# Página principal após login
st.image("logo_pioneer_240px.png", width=120)
st.markdown("<h1 style='text-align: center;'>Consulta de Peças e Modelos - Pioneer</h1>", unsafe_allow_html=True)
st.markdown("---")

col1, col2 = st.columns(2)
with col1:
    campo_busca = st.selectbox("Buscar por:", ["Código", "Modelo", "Descrição"])
with col2:
    tipo_busca = st.selectbox("Tipo de busca:", ["Contém", "Igual"])

codigo = st.text_input("Digite o código")

col3, col4 = st.columns([1, 1])
buscar = col3.button("🔍 Procurar")
limpar = col4.button("🧹 Limpar busca")

if limpar:
    st.session_state.resultado = pd.DataFrame()
    st.experimental_rerun()

# Simulando dados
@st.cache_data
def carregar_dados():
    data = {
        "Modelo": ["DMH-145BR", "DMH-A348BT", "DMH-ZS8280TV", "MVH-98UB"],
        "Código": ["QDP3071", "QDP3072", "01P0300021", "121104070007"],
        "Descrição": ["CABO PARA LIGACAO DE AUTO RADIO"] * 4,
        "Depósito": ["AGY3"] * 4,
        "Qtde.": [103, 52, 3, 352],
        "Valor Total": [1137.12, 42.50, 5.25, 2.85],
        "Categoria": ["Funcional"] * 4,
        "Início Fabricação": ["None"] * 4,
        "Término Fabricação": ["None"] * 4,
        "Qtde. Vendidas": ["None"] * 4
    }
    return pd.DataFrame(data)

df = carregar_dados()

if buscar and codigo:
    if tipo_busca == "Contém":
        resultado = df[df[campo_busca].str.contains(codigo, case=False, na=False)]
    else:
        resultado = df[df[campo_busca].str.lower() == codigo.lower()]
    if not resultado.empty:
        st.success(f"{len(resultado)} resultado(s) encontrado(s).")
        st.dataframe(resultado, use_container_width=True)
    else:
        st.warning("Nenhum resultado encontrado.")
