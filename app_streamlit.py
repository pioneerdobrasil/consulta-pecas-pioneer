
import streamlit as st
import json

st.set_page_config(page_title="Consulta de Peças e Modelos - Pioneer", layout="wide")

# Função para autenticar usuário
def autenticar_usuario(usuario, senha):
    try:
        with open("usuarios.json", "r") as f:
            usuarios = json.load(f)
        return usuarios.get(usuario) == senha
    except FileNotFoundError:
        return False

# Inicializar estado de autenticação
if "autenticado" not in st.session_state:
    st.session_state.autenticado = False
if "usuario" not in st.session_state:
    st.session_state.usuario = ""

# Tela de login
def login():
    st.image("logo.png", width=150)
    st.title("Login")
    usuario = st.text_input("Usuário")
    senha = st.text_input("Senha", type="password")
    if st.button("Entrar"):
        if autenticar_usuario(usuario, senha):
            st.session_state.autenticado = True
            st.session_state.usuario = usuario
            st.rerun()
        else:
            st.error("Usuário ou senha inválidos.")

# Tela principal
def app():
    st.image("logo.png", width=150)
    st.markdown(
        "<h1 style='text-align: center;'>Consulta de Peças e Modelos - Pioneer</h1>",
        unsafe_allow_html=True
    )
    st.markdown("---")
    col1, col2 = st.columns(2)
    with col1:
        campo_busca = st.selectbox("Buscar por:", ["Código", "Modelo", "Descrição"])
    with col2:
        tipo_busca = st.selectbox("Tipo de busca:", ["Contém", "Igual"])

    termo = st.text_input("Digite o código")
    col3, col4 = st.columns([1, 2])
    with col3:
        if st.button("🔍 Procurar"):
            st.success("Simulação de busca com: " + termo)
    with col4:
        if st.button("🧹 Limpar busca"):
            st.session_state.clear()
            st.rerun()

# Verifica autenticação
if not st.session_state.autenticado:
    login()
else:
    app()
