import streamlit as st
import pandas as pd
from datetime import datetime

# Inicializar st.session_state.atendimentos se ainda não existir
if 'atendimentos' not in st.session_state:
    st.session_state.atendimentos = []

# Função para salvar dados em um DataFrame
def save_data(nome, interessado, comunidade, municipio, fone, email, protocolo, data, motivo):
    new_data = {
        "Nome": nome,
        "Interessado": interessado,
        "Comunidade": comunidade,
        "Município": municipio,
        "Telefone": fone,
        "Email": email,
        "Protocolo SEI": protocolo,
        "Data": data,
        "Motivo do Atendimento": motivo
    }
    return new_data

# Função para exportar dados para Excel
def export_to_excel(df):
    df.to_excel('atendimentos.xlsx', index=False)
    st.success("Dados exportados com sucesso para atendimentos.xlsx")

# Interface do Formulário usando Streamlit
st.markdown('<h1 style="color: blue;">Registro de Atendimentos da Divisão Quilombola_SR-MA</h1>', unsafe_allow_html=True)

# Campos do Formulário
nome = st.text_input("Nome do Atendente")
interessado = st.text_input("Nome do Interessado")
comunidade = st.text_input("Comunidade")
municipio = st.text_input("Município")
fone = st.text_input("Telefone")
email = st.text_input("Email")
protocolo = st.text_input("Protocolo SEI")
data = st.date_input("Data", datetime.today())
motivo = st.text_area("Motivo do Atendimento")

# Botões
if st.button("Salvar"):
    if nome:
        atendimento_data = save_data(nome, interessado, comunidade, municipio, fone, email, protocolo, data, motivo)
        st.session_state.atendimentos.append(atendimento_data)
        st.success(f"Obrigado, {nome}. Seus dados foram salvos com sucesso!")
    else:
        st.error("Por favor, preencha o campo 'Nome'.")

if st.button("Exportar para Excel"):
    if st.session_state.atendimentos:
        df = pd.DataFrame(st.session_state.atendimentos)
        export_to_excel(df)
    else:
        st.warning("Nenhum dado disponível para exportação.")

# Mostrar Dados Salvos
if st.session_state.atendimentos:
    st.subheader("Dados Salvos")
    st.dataframe(pd.DataFrame(st.session_state.atendimentos))

