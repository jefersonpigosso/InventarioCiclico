import streamlit as st
import requests
import pandas as pd

# Configuração de layout para tela cheia
st.set_page_config(page_title="Consulta de Endereço", layout="wide")

# Título da aplicação
st.title("Consulta de Endereço")

# Input para o usuário inserir o endereço
endereco = st.text_input("Insira o endereço:")

# Função para fazer a requisição e exibir os dados
def consultar_endereco(endereco):
    # URL da API
    url = 'http://172.16.103.71:85/api/EnderecamentoConsulta'
    
    # Headers e payload para enviar o endereço como dado JSON
    headers = {
        'Content-Type': 'application/json',
    }
    payload = {
        "endereco": endereco
    }
    
    try:
        # Faz a requisição PATCH
        response = requests.patch(url, headers=headers, json=payload)
        
        # Verifica o sucesso da requisição
        if response.status_code == 200:
            # Converte a resposta JSON para DataFrame
            dados = response.json()
            df = pd.json_normalize(dados)  # Normaliza para uma tabela
            return df
        else:
            st.error(f"Erro: {response.status_code} - {response.text}")
            return None
    except requests.exceptions.RequestException as e:
        st.error(f"Erro na requisição: {e}")
        return None

# Botão para consultar
if st.button("Consultar"):
    if endereco:
        # Chama a função de consulta e exibe a tabela, se houver dados
        df = consultar_endereco(endereco)
        if df is not None:
            st.write("Dados do Endereço:")
            st.table(df)
    else:
        st.warning("Por favor, insira um endereço.")
