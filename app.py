import streamlit as st
import pandas as pd
import sqlite3
from datetime import datetime

# Funções para Banco de Dados
def iniciar_banco_de_dados():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS atendimentos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            atendente TEXT,
            interessado TEXT,
            comunidade TEXT,
            municipio TEXT,
            telefone TEXT,
            email TEXT,
            protocolo TEXT,
            data DATE,
            motivo TEXT
        )
    ''')
    conn.commit()
    conn.close()

def adicionar_registro(atendente, interessado, comunidade, municipio, telefone, email, protocolo, data, motivo):
    if isinstance(data, datetime):
        data = data.strftime("%Y-%m-%d")

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO atendimentos (atendente, interessado, comunidade, municipio, telefone, email, protocolo, data, motivo)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (atendente, interessado, comunidade, municipio, telefone, email, protocolo, data, motivo))
    conn.commit()
    conn.close()

def obter_todos_os_registros():
    conn = sqlite3.connect('database.db')
    df = pd.read_sql_query('SELECT * FROM atendimentos', conn)
    conn.close()
  
    return df

iniciar_banco_de_dados()

# Interface com Streamlit
st.markdown('<h1 style="color: blue;">Registro de Atendimentos da Divisão Quilombola</h1>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    atendente = st.text_input("Nome do Atendente", max_chars=50, key="atendente", help="Digite o nome do Atendente")
    interessado = st.text_input("Nome do Interessado", max_chars=50, key="nome_interessado")
    telefone = st.text_input("Telefone", max_chars=11, key="fone")
    protocolo = st.text_input("Protocolo SEI", max_chars=10, key="protocolo")

with col2:
    comunidade = st.text_input("Comunidade")
    municipio = st.text_input("Município")
    email = st.text_input("Email")
    data = st.date_input("Data", datetime.today())

motivo = st.text_area("Motivo do Atendimento", height=100, help="Digite o motivo do atendimento")

if st.button("Salvar"):
    if atendente:
        adicionar_registro(atendente, interessado, comunidade, municipio, telefone, email, protocolo, data, motivo)
        st.success(f"Obrigado, {atendente}. Os dados foram salvos com sucesso!")
    else:
        st.error("Por favor, preencha o campo 'Nome'.")

st.subheader("Registros Salvos")
df = obter_todos_os_registros()
# Ocultar a coluna 'id' e ajustar o índice para começar em 1
if 'id' in df.columns:
    df = df.drop(columns=['id'])  # Remove a coluna 'id'
df.index = df.index + 1  # Ajusta o índice para começar em 1
st.dataframe(df)

if st.button("Exportar para Excel"):
    df.to_excel('atendimentos.xlsx', index=False)
    st.success("Dados exportados com sucesso para atendimentos.xlsx")
    with open("atendimentos.xlsx", "rb") as file:
        st.download_button(
            label="Baixar Excel",
            data=file,
            file_name="atendimentos.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )