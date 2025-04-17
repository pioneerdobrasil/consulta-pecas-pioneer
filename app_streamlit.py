
import streamlit as st
import pandas as pd
import json

# --- Função de autenticação ---
def autenticar_usuario(usuario, senha):
    with open("usuarios.json", "r") as f:
        usuarios = json.load(f)
    return usuarios.get(usuario) == senha

# --- Função para carregar dados ---
def carregar_dados():
    try:
        return pd.read_excel("Referência_Cruzada_2_Atualizada.xlsx")
    except Exception as e:
        st.error(f"Erro ao carregar os dados: {e}")
        return None

# --- Página de login ---
if "autenticado" not in st.session_state:
    st.session_state.autenticado = False

if not st.session_state.autenticado:
    st.image("logo_pioneer_240px.png", width=150)
    st.title("Login")

    usuario = st.text_input("Usuário")
    senha = st.text_input("Senha", type="password")
    if st.button("Entrar"):
        if autenticar_usuario(usuario, senha):
            st.session_state.autenticado = True
            st.rerun()
        else:
            st.error("Usuário ou senha inválidos.")
    st.stop()

# --- Interface principal ---
st.image("logo_pioneer_240px.png", width=100)
st.markdown("<h1 style='text-align: center;'>Consulta de Peças e Modelos - Pioneer</h1>", unsafe_allow_html=True)

# Filtros
opcao_busca = st.selectbox("Buscar por:", ["Código", "Modelo", "Descrição", "Categoria", "Depósito"])
tipo_busca = st.selectbox("Tipo de busca:", ["Contém", "Igual"])
texto_busca = st.text_input("Digite o código")

dados = carregar_dados()
if dados is not None:
    if st.button("🔍 Procurar"):
        if texto_busca:
            if tipo_busca == "Contém":
                resultado = dados[dados[opcao_busca].astype(str).str.contains(texto_busca, case=False, na=False)]
            else:
                resultado = dados[dados[opcao_busca].astype(str) == texto_busca]
            if not resultado.empty:
                st.success(f"{len(resultado)} resultado(s) encontrado(s).")
                st.dataframe(resultado, use_container_width=True)
            else:
                st.warning("Nenhum resultado encontrado.")
        else:
            st.warning("Digite um valor para busca.")
    if st.button("🧹 Limpar busca"):
        st.rerun()
