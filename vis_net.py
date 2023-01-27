import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import networkx as nx
from pyvis.network import Network
import itertools

st.title('Visualizando sua rede de conexões do Linkedin')
st.write("""
Este projeto utiliza dados de sua conta disponíveis no próprio Linkedin, 
priorizando relacionamentos com mais de um nó.\n
Para obter seus dados, siga o link: https://www.linkedin.com/help/linkedin/answer/a566336/export-connections-from-linkedin
\n\n
""")
upload_file = st.file_uploader('Escolha um arquivo:')

if upload_file is not None:
    connections = pd.read_csv(upload_file)
    buttom = st.button('Visualizar a rede - **_Aguarde a barra de progresso carregar_**')
    st.dataframe(connections)
# connections = pd.read_csv('Connections.csv')



    if buttom:
        H = nx.Graph(notebook=True)

        for i in connections.index:
            H.add_node(i+1)

        nome = dict(connections['First Name'])
        company = dict(connections['Company'])

        nx.set_node_attributes(H, nome, "title")
        nx.set_node_attributes(H, company, "group")

        H.nodes[connections.index[-1]+1]["title"] = "Você"
        H.nodes[connections.index[-1]+1]["group"] = "Onde voce trabalha"

        for i in connections.index:
            H.add_edge(i, connections.index[-1]+1)

        companies = dict()

        for company in set(connections["Company"]):
            companies[company] = list(connections[connections["Company"] == company].index)

        for company in companies.keys():
            H.add_edges_from(list(itertools.combinations(companies[company], 2)))
        low_deg = [node for node in H.nodes if len(list(nx.neighbors(H, node))) == 1]
        H.remove_nodes_from(low_deg)
        nt = Network('500px', '500px')
        nt.from_nx(H)
        nt.show('nt.html', local=True)
        HtmlFile = open("nt.html", 'r', encoding='utf-8')
        source_code = HtmlFile.read() 
        components.html(source_code, height = 1200,width=1000)
        
st.warning("""
Caso você não se sinta confortável em fazer o upload dos seus dados, clique no botão abaixo para 
utilizar dados aleatórios
""")
buttom_random = st.button('Visualizar rede com dados aleatórios - **_Aguarda a barra de progresso carregar_**')
if buttom_random:
    random_file = 'Connections-random-names.csv'
    connections = pd.read_csv(random_file)
    H = nx.Graph(notebook=True)

    for i in connections.index:
        H.add_node(i + 1)

    nome = dict(connections['First Name'])
    company = dict(connections['Company'])

    nx.set_node_attributes(H, nome, "title")
    nx.set_node_attributes(H, company, "group")

    H.nodes[connections.index[-1] + 1]["title"] = "Você"
    H.nodes[connections.index[-1] + 1]["group"] = "Onde voce trabalha"

    for i in connections.index:
        H.add_edge(i, connections.index[-1] + 1)

    companies = dict()

    for company in set(connections["Company"]):
        companies[company] = list(connections[connections["Company"] == company].index)

    for company in companies.keys():
        H.add_edges_from(list(itertools.combinations(companies[company], 2)))
    low_deg = [node for node in H.nodes if len(list(nx.neighbors(H, node))) == 1]
    H.remove_nodes_from(low_deg)
    nt = Network('500px', '500px')
    nt.from_nx(H)
    nt.show('nt.html', local=True)
    HtmlFile = open("nt.html", 'r', encoding='utf-8')
    source_code = HtmlFile.read() 
    components.html(source_code, height = 1200,width=1000)
