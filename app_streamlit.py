
import streamlit as st
import pandas as pd
from io import BytesIO

# Função para converter DataFrame em Excel sem salvar no disco
def to_excel_download(df):
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Resultado')
    processed_data = output.getvalue()
    return processed_data

# Layout da interface
st.image("logo_pioneer_240px.png", width=200)
st.markdown("<h1 style='text-align: center;'>Consulta de Peças e Modelos - Pioneer</h1>", unsafe_allow_html=True)

# Carregamento de dados
@st.cache_data
def carregar_dados():
    return pd.read_excel("Referência_Cruzada_2_Atualizada.xlsx")

df = carregar_dados()

# Filtros
col1, col2 = st.columns(2)
campo = col1.selectbox("Buscar por:", df.columns.tolist())
tipo_busca = col2.selectbox("Tipo de busca:", ["Contém", "Igual"])

termo = st.text_input("Digite o código")

col3, col4 = st.columns([1, 2])
procurar = col3.button("🔍 Procurar")
limpar = col4.button("🧹 Limpar busca")

resultado = pd.DataFrame()

if procurar and termo:
    if tipo_busca == "Contém":
        resultado = df[df[campo].astype(str).str.contains(termo, case=False, na=False)]
    elif tipo_busca == "Igual":
        resultado = df[df[campo].astype(str) == termo]

    st.success(f"{len(resultado)} resultado(s) encontrado(s).")

    if not resultado.empty:
        st.dataframe(resultado)

        # Exportar CSV
        csv = resultado.to_csv(index=False).encode("utf-8")
        st.download_button("📄 Baixar CSV", csv, "resultado.csv", "text/csv")

        # Exportar Excel
        excel_data = to_excel_download(resultado)
        st.download_button("📊 Baixar Excel", excel_data, "resultado.xlsx", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

elif limpar:
    st.experimental_rerun()
