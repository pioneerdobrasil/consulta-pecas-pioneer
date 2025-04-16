
import streamlit as st
import pandas as pd
import io

@st.cache_data(show_spinner=False)
def carregar_dados():
    df = pd.read_excel("Referência_Cruzada_2_Atualizada.xlsx")

    # Normalização para evitar problemas de busca
    df["Código"] = df["Código"].astype(str).str.strip().str.upper()
    df["Modelo"] = df["Modelo"].astype(str).str.strip().str.upper()

    return df

st.title("Consulta de Peças e Modelos - Pioneer")

if st.button("🔄 Recarregar banco de dados"):
    st.cache_data.clear()

df = carregar_dados()

col1, col2 = st.columns(2)
with col1:
    campo = st.selectbox("Buscar por:", ["Código", "Modelo"])
with col2:
    tipo_busca = st.selectbox("Tipo de busca:", ["Contém", "Começa com", "Igual"])

entrada = st.text_input(f"Digite o {campo.lower()}").strip().upper()

resultado = pd.DataFrame()
if entrada:
    if tipo_busca == "Contém":
        resultado = df[df[campo].str.contains(entrada, case=False, na=False)]
    elif tipo_busca == "Começa com":
        resultado = df[df[campo].str.startswith(entrada)]
    elif tipo_busca == "Igual":
        resultado = df[df[campo] == entrada]

if st.button("🧹 Limpar busca"):
    st.experimental_rerun()

if not resultado.empty:
    st.success(f"{len(resultado)} resultado(s) encontrado(s).")
    st.dataframe(resultado)

    csv = resultado.to_csv(index=False).encode('utf-8')
    st.download_button("⬇️ Baixar CSV", data=csv, file_name="resultado.csv", mime="text/csv")

    buffer = io.BytesIO()
    with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
        resultado.to_excel(writer, index=False, sheet_name="Resultados")
    st.download_button("⬇️ Baixar Excel", data=buffer.getvalue(), file_name="resultado.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
elif entrada:
    st.warning("Nenhum resultado encontrado.")
