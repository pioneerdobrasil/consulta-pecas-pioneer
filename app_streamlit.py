
import streamlit as st
import pandas as pd

# Configuração da página
st.set_page_config(page_title="Consulta de Peças - Pioneer", layout="wide")

# Função para carregar dados com cache
@st.cache_data
def carregar_dados():
    return pd.read_excel("Referência_Cruzada_2_Atualizada.xlsx")

# Layout do cabeçalho com imagem
col_logo, col_titulo = st.columns([1, 8])
with col_logo:
    st.image("logo_pioneer_240px.png", width=180)
with col_titulo:
    st.markdown("<h1 style='text-align: center;'>Consulta de Peças e Modelos - Pioneer</h1>", unsafe_allow_html=True)

# Carregamento do DataFrame
df = carregar_dados()

# Exibir colunas detectadas
with st.sidebar:
    st.markdown("### 🧾 Colunas detectadas:")
    for col in df.columns:
        st.markdown(f"- {col}")

# Filtros de busca
col1, col2 = st.columns(2)
with col1:
    campo = st.selectbox("Buscar por:", df.columns.tolist(), index=0)
with col2:
    tipo_busca = st.selectbox("Tipo de busca:", ["Contém", "Igual", "Inicia com", "Termina com"], index=0)

# Campo de entrada de texto
texto_busca = st.text_input(f"Digite o {campo.lower()}")

# Botões de ação
col_botao1, col_botao2 = st.columns([1, 6])
buscar = col_botao1.button("🔍 Procurar")
limpar = col_botao2.button("🧹 Limpar busca")

# Ações dos botões
if buscar and texto_busca:
    if tipo_busca == "Contém":
        resultado = df[df[campo].astype(str).str.contains(texto_busca, case=False, na=False)]
    elif tipo_busca == "Igual":
        resultado = df[df[campo].astype(str).str.lower() == texto_busca.lower()]
    elif tipo_busca == "Inicia com":
        resultado = df[df[campo].astype(str).str.startswith(texto_busca)]
    elif tipo_busca == "Termina com":
        resultado = df[df[campo].astype(str).str.endswith(texto_busca)]
    else:
        resultado = pd.DataFrame()
    
    st.success(f"{len(resultado)} resultado(s) encontrado(s).")
    st.dataframe(resultado, use_container_width=True)
    
    if not resultado.empty:
        col3, col4 = st.columns(2)
        with col3:
            st.download_button("📄 Baixar CSV", resultado.to_csv(index=False).encode('utf-8'), "resultado.csv", "text/csv")
        with col4:
            st.download_button("📊 Baixar Excel", resultado.to_excel(index=False, engine="openpyxl"), "resultado.xlsx", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
elif limpar:
    st.experimental_rerun()
