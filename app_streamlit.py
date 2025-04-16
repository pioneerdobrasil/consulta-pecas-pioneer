
import streamlit as st
import pandas as pd

st.set_page_config(layout="wide")
st.markdown("<h1 style='text-align: center;'>Consulta de Peças e Modelos - Pioneer</h1>", unsafe_allow_html=True)

# Simula carregamento de dados
dados = pd.DataFrame({
    "Modelo": ["DEH-X5000BR", "DEH-X5000BR"],
    "Código": ["QDP3072-B/N", "QDP3072-B/N"],
    "Descrição": ["CONJUNTO DE CABOSCONDUTORES ISOLADOS"] * 2,
    "Depósito": ["AGY3", "AGY3"],
    "Qtde.": [1987, 1987],
    "Valor Total": [12787.57, 12787.57],
    "Categoria": ["Funcional", "Funcional"],
    "Início Fabricação": ["2019-08-26 00:00:00", "2018-09-25 00:00:00"],
    "Término Fabricação": ["2020-07-31 00:00:00", "2019-08-21 00:00:00"]
})

codigo = st.text_input("Digite o código")

if st.button("Procurar"):
    resultado = dados[dados["Código"].str.contains(codigo)]
    if not resultado.empty:
        st.success(f"{len(resultado)} resultado(s) encontrado(s).")
        st.dataframe(resultado, use_container_width=True)
    else:
        st.warning("Nenhum resultado encontrado.")
