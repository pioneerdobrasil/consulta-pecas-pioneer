
import streamlit as st
import pandas as pd

# Centralizar conteúdo e remover menu/hambúrguer
st.set_page_config(page_title="Consulta de Peças e Modelos", layout="wide", page_icon="🔍")

# Ocultar elementos padrão do Streamlit
hide_st_style = '''
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
</style>
'''
st.markdown(hide_st_style, unsafe_allow_html=True)

# Layout da logo e título
col_logo, col_title, _ = st.columns([1, 3, 1])
with col_logo:
    st.image("logo.png", width=180)
with col_title:
    st.markdown("## Consulta de Peças e Modelos - Pioneer")

# Carregamento dos dados
@st.cache_data
def carregar_dados():
    return pd.read_excel("Referência_Cruzada_2_Atualizada.xlsx")

df = carregar_dados()

# Lateral com colunas detectadas
with st.sidebar:
    st.markdown("### 🗂️ Colunas detectadas:")
    for col in df.columns:
        st.markdown(f"- {col}")

# Filtros de busca
col1, col2 = st.columns([1, 3])
opcoes_coluna = df.columns.tolist()

with col1:
    coluna = st.selectbox("Buscar por:", opcoes_coluna)
with col2:
    tipo_busca = st.selectbox("Tipo de busca:", ["Contém", "Igual"])

valor = st.text_input("Digite o código")

# Botões
col_buscar, col_limpar = st.columns([1, 1])
buscar = col_buscar.button("🔍 Procurar")
limpar = col_limpar.button("🧹 Limpar busca")

# Execução da busca
if buscar and valor:
    if tipo_busca == "Contém":
        resultado = df[df[coluna].astype(str).str.contains(valor, case=False, na=False)]
    else:
        resultado = df[df[coluna].astype(str).str.lower() == valor.lower()]

    qtd = len(resultado)
    st.success(f"{qtd} resultado(s) encontrado(s).")
    st.dataframe(resultado, use_container_width=True)

    # Exportar resultados
    col_export1, col_export2 = st.columns([1, 1])
    col_export1.download_button("⬇️ Baixar CSV", data=resultado.to_csv(index=False).encode("utf-8"), file_name="resultado.csv", mime="text/csv")
    col_export2.download_button("⬇️ Baixar Excel", data=resultado.to_excel(index=False, engine="openpyxl"), file_name="resultado.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

# Limpar filtros
if limpar:
    st.rerun()
