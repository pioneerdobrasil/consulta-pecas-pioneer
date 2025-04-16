
import streamlit as st
import pandas as pd
import json

# Função para autenticação
def autenticar_usuario(usuario, senha):
    with open("usuarios.json", "r") as f:
        usuarios = json.load(f)
    return usuario in usuarios and usuarios[usuario] == senha

# Inicialização de sessão
if "autenticado" not in st.session_state:
    st.session_state["autenticado"] = False
    st.session_state["usuario"] = ""

# Tela de login
if not st.session_state["autenticado"]:
    st.image("logo_pioneer_240px.png", width=100)
    st.title("Login")

    usuario = st.text_input("Usuário")
    senha = st.text_input("Senha", type="password")

    if st.button("Entrar"):
        if autenticar_usuario(usuario, senha):
            st.session_state["autenticado"] = True
            st.session_state["usuario"] = usuario
            st.experimental_rerun()
        else:
            st.error("Usuário ou senha inválidos")
else:
    # Interface principal do sistema
    st.image("logo_pioneer_240px.png", width=100)
    st.markdown("<h1 style='text-align: center;'>Consulta de Peças e Modelos - Pioneer</h1>", unsafe_allow_html=True)

    uploaded_file = st.file_uploader("Envie sua planilha Excel", type=["xlsx"])
    if uploaded_file:
        df = pd.read_excel(uploaded_file)
        st.session_state["dataframe"] = df

    if "dataframe" in st.session_state:
        df = st.session_state["dataframe"]
        col1, col2 = st.columns(2)
        with col1:
            coluna_busca = st.selectbox("Buscar por:", df.columns.tolist())
        with col2:
            tipo_busca = st.selectbox("Tipo de busca:", ["Contém", "Igual"])

        termo = st.text_input("Digite o código")
        col1, col2 = st.columns([1, 2])
        with col1:
            buscar = st.button("🔍 Procurar")
        with col2:
            limpar = st.button("🧹 Limpar busca")

        if buscar:
            if tipo_busca == "Contém":
                resultado = df[df[coluna_busca].astype(str).str.contains(termo, case=False, na=False)]
            else:
                resultado = df[df[coluna_busca].astype(str) == termo]
            st.session_state["resultado"] = resultado
        elif limpar:
            if "resultado" in st.session_state:
                del st.session_state["resultado"]
            st.experimental_rerun()

        if "resultado" in st.session_state:
            resultado = st.session_state["resultado"]
            st.success(f"{len(resultado)} resultado(s) encontrado(s).")
            st.dataframe(resultado, use_container_width=True)
