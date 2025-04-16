
import streamlit as st
import pandas as pd
import json

st.set_page_config(page_title="Consulta de Peças Pioneer", layout="wide")

# Função de autenticação
def autenticar_usuario(usuario, senha):
    try:
        with open("usuarios.json", "r") as f:
            usuarios = json.load(f)
        return usuarios.get(usuario) == senha
    except FileNotFoundError:
        return False

# Função para exibir o login
def exibir_login():
    st.image("logo_pioneer_240px.png", width=150)
    st.markdown("## Login")
    usuario = st.text_input("Usuário")
    senha = st.text_input("Senha", type="password")
    if st.button("Entrar"):
        if autenticar_usuario(usuario, senha):
            st.session_state["autenticado"] = True
            st.rerun()
        else:
            st.error("Usuário ou senha inválidos.")

# Função principal do app
def main_app():
    st.image("logo_pioneer_240px.png", width=150)
    st.markdown("<h1 style='text-align: center;'>Consulta de Peças e Modelos - Pioneer</h1>", unsafe_allow_html=True)
    
    # Carregamento simulado do DataFrame (substitua com seu carregamento real)
    try:
        df = pd.read_excel("Referência_Cruzada_2_Atualizada.xlsx")
    except FileNotFoundError:
        st.error("Arquivo de dados não encontrado.")
        return

    col1, col2 = st.columns(2)
    with col1:
        campo_busca = st.selectbox("Buscar por:", df.columns.tolist())
    with col2:
        tipo_busca = st.selectbox("Tipo de busca:", ["Contém", "Igual", "Começa com"])

    termo_busca = st.text_input("Digite o código")
    col3, col4 = st.columns(2)
    with col3:
        if st.button("🔍 Procurar"):
            if termo_busca:
                if tipo_busca == "Contém":
                    resultado = df[df[campo_busca].astype(str).str.contains(termo_busca, case=False, na=False)]
                elif tipo_busca == "Igual":
                    resultado = df[df[campo_busca].astype(str) == termo_busca]
                elif tipo_busca == "Começa com":
                    resultado = df[df[campo_busca].astype(str).str.startswith(termo_busca)]
                else:
                    resultado = pd.DataFrame()
                if not resultado.empty:
                    st.success(f"{len(resultado)} resultado(s) encontrado(s).")
                    st.dataframe(resultado, use_container_width=True)
                else:
                    st.warning("Nenhum resultado encontrado.")
            else:
                st.warning("Digite um termo para buscar.")
    with col4:
        if st.button("🧹 Limpar busca"):
            st.rerun()

# Controle de autenticação
if "autenticado" not in st.session_state:
    st.session_state["autenticado"] = False

if not st.session_state["autenticado"]:
    exibir_login()
else:
    main_app()
