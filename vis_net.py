import streamlit as st
import pandas as pd
from functions import create_network, visualize_network


st.title('Visualizando sua rede de conexões do Linkedin')
st.write("""
Este projeto utiliza dados de sua conta disponíveis no próprio Linkedin, 
priorizando relacionamentos com mais de um nó.\n
Para obter seus dados, siga o link: https://www.linkedin.com/help/linkedin/answer/a566336/export-connections-from-linkedin
\n\n
""")

upload_file = st.file_uploader('Escolha um arquivo:')

if upload_file is not None:
    connections = pd.read_csv(upload_file, skiprows=3)
    button = st.button('Visualizar a rede - **_Aguarde a barra de progresso carregar_**')
    
    if button is False:
        st.dataframe(connections)

    else:
        H = create_network(connections)
        visualize_network(H)

st.warning("""
Caso você não se sinta confortável em fazer o upload dos seus dados, clique no botão abaixo para 
utilizar dados aleatórios
""")

button_random = st.button('Visualizar rede com dados aleatórios - **_Aguarda a barra de progresso carregar_**')

if button_random:
    random_file = 'Connections-random-names.csv'
    connections = pd.read_csv(random_file)
    H = create_network(connections)
    visualize_network(H)
