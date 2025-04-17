
import streamlit as st
import pandas as pd
import json

# Função para autenticar usuário
def autenticar_usuario(usuario, senha):
    try:
        with open("usuarios.json", "r") as f:
            usuarios = json.load(f)
        return usuarios.get(usuario) == senha
    except FileNotFoundError:
        return False

# Função principal da aplicação
def main():
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
                st.rerun()
            else:
                st.error("Usuário ou senha incorretos.")
    else:
        st.image("logo_pioneer_240px.png", width=120)
        st.markdown("<h1 style='text-align: center;'>Consulta de Peças e Modelos - Pioneer</h1>", unsafe_allow_html=True)

        # Filtros
        opcao_busca = st.selectbox("Buscar por:", ["Código", "Modelo"])
        tipo_busca = st.selectbox("Tipo de busca:", ["Contém", "Igual"])
        termo = st.text_input("Digite o código")

        if st.button("🔍 Procurar"):
            try:
                df = pd.read_excel("Estoque_20250414.xlsx")
                coluna = "Código" if opcao_busca == "Código" else "Modelo"
                if tipo_busca == "Contém":
                    resultado = df[df[coluna].astype(str).str.contains(termo, case=False, na=False)]
                else:
                    resultado = df[df[coluna].astype(str) == termo]
                if not resultado.empty:
                    st.success(f"{len(resultado)} resultado(s) encontrado(s).")
                    st.dataframe(resultado, use_container_width=True)
                else:
                    st.warning("Nenhum resultado encontrado.")
            except Exception as e:
                st.error(f"Erro ao carregar os dados: {e}")

        if st.button("🪄 Limpar busca"):
            st.session_state.clear()
            st.rerun()

if __name__ == "__main__":
    main()
