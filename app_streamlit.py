
import streamlit as st
import pandas as pd
import json
import hashlib

# --- Funções de autenticação ---
def carregar_usuarios():
    with open("usuarios.json", "r") as f:
        return json.load(f)

def autenticar_usuario(usuario, senha):
    usuarios = carregar_usuarios()
    senha_hash = hashlib.sha256(senha.encode()).hexdigest()
    return usuarios.get(usuario) == senha_hash

def login():
    st.image("logo_pioneer_240px.png", width=120)
    st.title("Login")

    usuario = st.text_input("Usuário")
    senha = st.text_input("Senha", type="password")

    if st.button("Entrar"):
        if autenticar_usuario(usuario, senha):
            st.session_state["autenticado"] = True
            st.session_state["usuario"] = usuario
            st.rerun()
        else:
            st.error("Usuário ou senha inválidos.")

# --- Função principal ---
def main():
    st.image("logo_pioneer_240px.png", width=120)
    st.markdown("<h1 style='text-align: center;'>Consulta de Peças e Modelos - Pioneer</h1>", unsafe_allow_html=True)

    df = pd.read_excel("Referência_Cruzada_2_Atualizada.xlsx")

    col1, col2 = st.columns(2)
    with col1:
        filtro_coluna = st.selectbox("Buscar por:", df.columns.tolist())
    with col2:
        tipo_busca = st.selectbox("Tipo de busca:", ["Contém", "Igual", "Começa com"])

    valor_busca = st.text_input("Digite o código")

    col3, col4 = st.columns([1, 5])
    with col3:
        if st.button("🔍 Procurar"):
            if tipo_busca == "Contém":
                resultado = df[df[filtro_coluna].astype(str).str.contains(valor_busca, case=False, na=False)]
            elif tipo_busca == "Igual":
                resultado = df[df[filtro_coluna].astype(str) == valor_busca]
            elif tipo_busca == "Começa com":
                resultado = df[df[filtro_coluna].astype(str).str.startswith(valor_busca)]
            else:
                resultado = pd.DataFrame()

            if not resultado.empty:
                st.success(f"{len(resultado)} resultado(s) encontrado(s).")
                st.dataframe(resultado, use_container_width=True)
            else:
                st.warning("Nenhum resultado encontrado.")
    with col4:
        if st.button("🧹 Limpar busca"):
            st.rerun()

# --- Execução ---
if "autenticado" not in st.session_state or not st.session_state["autenticado"]:
    login()
else:
    main()
