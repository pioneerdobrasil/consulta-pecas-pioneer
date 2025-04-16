
import streamlit as st
import pandas as pd
import io

# Inicializar estado da busca se necessário
if "busca" not in st.session_state:
    st.session_state.busca = ""

@st.cache_data(show_spinner=False)
def carregar_dados():
    df = pd.read_excel("Referência_Cruzada_2_Atualizada.xlsx")

    st.sidebar.subheader("🧪 Colunas detectadas:")
    for col in df.columns:
        st.sidebar.write("-", col)

    df.columns = df.columns.str.strip().str.lower()

    codigo_col = next((col for col in df.columns if "código" in col), None)
    modelo_col = next((col for col in df.columns if "modelo" in col), None)

    if not codigo_col or not modelo_col:
        st.error("As colunas 'Código' ou 'Modelo' não foram encontradas.")
        return pd.DataFrame(), None, None

    df[codigo_col] = df[codigo_col].astype(str).str.strip().str.upper()
    df[modelo_col] = df[modelo_col].astype(str).str.strip().str.upper()

    return df, codigo_col, modelo_col

st.title("Consulta de Peças e Modelos - Pioneer")

if st.button("🔄 Recarregar banco de dados"):
    st.cache_data.clear()

df, codigo_col, modelo_col = carregar_dados()

if df.empty:
    st.stop()

col1, col2 = st.columns(2)
with col1:
    campo_opcao = st.selectbox("Buscar por:", ["Código", "Modelo"])
with col2:
    tipo_busca = st.selectbox("Tipo de busca:", ["Contém", "Começa com", "Igual"])

# Input com estado
entrada = st.text_input(f"Digite o {campo_opcao.lower()}", value=st.session_state.busca).strip().upper()

# Salva nova entrada (caso digitada manualmente)
if entrada != st.session_state.busca:
    st.session_state.busca = entrada

campo = codigo_col if campo_opcao == "Código" else modelo_col
resultado = pd.DataFrame()

if st.session_state.busca:
    if tipo_busca == "Contém":
        resultado = df[df[campo].str.contains(st.session_state.busca, na=False)]
    elif tipo_busca == "Começa com":
        resultado = df[df[campo].str.startswith(st.session_state.busca)]
    elif tipo_busca == "Igual":
        resultado = df[df[campo] == st.session_state.busca]

# Botão para limpar busca de forma funcional
if st.button("🧹 Limpar busca"):
    st.session_state.busca = ""
    st.rerun()

if not resultado.empty:
    st.success(f"{len(resultado)} resultado(s) encontrado(s).")
    st.dataframe(resultado)

    csv = resultado.to_csv(index=False).encode('utf-8')
    st.download_button("⬇️ Baixar CSV", data=csv, file_name="resultado.csv", mime="text/csv")

    buffer = io.BytesIO()
    with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
        resultado.to_excel(writer, index=False, sheet_name="Resultados")
    st.download_button("⬇️ Baixar Excel", data=buffer.getvalue(), file_name="resultado.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
elif st.session_state.busca:
    st.warning("Nenhum resultado encontrado.")
