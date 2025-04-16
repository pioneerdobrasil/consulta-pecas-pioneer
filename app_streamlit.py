
import streamlit as st
import pandas as pd

# Carrega a planilha
df = pd.read_excel("Referência_Cruzada_2_Atualizada.xlsx")

# Título do app
st.title("Consulta de Peças e Modelos - Pioneer")

# Escolher critério de busca
opcao = st.selectbox("Buscar por:", ["Código", "Modelo"])

# Entrada de texto para busca
entrada = st.text_input(f"Digite o {opcao.lower()}")

# Resultado da busca
if entrada:
    resultado = df[df[opcao].astype(str).str.contains(entrada, case=False, na=False)]
    if not resultado.empty:
        st.success(f"{len(resultado)} resultado(s) encontrado(s).")
        st.dataframe(resultado, use_container_width=True)
    else:
        st.warning("Nenhum resultado encontrado.")
