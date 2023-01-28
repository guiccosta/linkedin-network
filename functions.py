import streamlit.components.v1 as components
import networkx as nx
from pyvis.network import Network

import itertools


def create_network(connections):
    """
    Retorna uma rede das conexões provenientes do arquivo Connections.csv fornecido pelo usuário, obtido
    diretamente do LinkedIn.
    :param connections: dataframe .csv
    :return: H networkx graph
    """

    h = nx.Graph(notebook=True)

    for i in connections.index:
        h.add_node(i + 1)

    name = dict(connections['First Name'])
    company = dict(connections['Company'])

    nx.set_node_attributes(h, name, "title")
    nx.set_node_attributes(h, company, "group")

    # Criando um nó para você já que no arquivo Connections.csv não possui essa informação
    # para isso, deixaremos o último nó para esta finalidade
    # os nós estão indexados pelo index do dataframe, por isso vamos usar connections.index[-1] + 1
    h.nodes[connections.index[-1] + 1]["title"] = "Você"
    h.nodes[connections.index[-1] + 1]["group"] = "Onde voce trabalha"

    for i in connections.index:
        h.add_edge(i, connections.index[-1] + 1)

    companies = dict()

    for company in set(connections["Company"]):
        # pessoas que trabalham na mesma Company
        nodes_same_company = list(connections[connections["Company"] == company].index)
        companies[company] = nodes_same_company

    for _, nodes in companies.items():
        # criando relacionamento entre as pessoas que trabalham na mesma Company
        edges_same_company = list(itertools.combinations(nodes, 2))
        h.add_edges_from(edges_same_company)

    low_deg = [node for node in h.nodes if len(list(nx.neighbors(h, node))) == 1]
    h.remove_nodes_from(low_deg)
    return h


def visualize_network(h: nx.classes.graph.Graph):
    """
    Visualiza a rede h.

    :param h: networkx graph
    """
    nt = Network('500px', '500px')
    nt.from_nx(h)
    nt.show('nt.html', local=False)

    with open('nt.html', 'r') as file:
        htmlfile = file
        source_code = htmlfile.read()
        components.html(source_code, height=500, width=500)
