# REFERÊNCIA(S): -------------------------------------------------------------------------------------------------------

# [1] https://www.youtube.com/watch?v=JcfIeaGzF8A
# [2] https://www.youtube.com/watch?v=EUQY3hL38cw

# PACOTE(S): -----------------------------------------------------------------------------------------------------------
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import time as time

# Métodos Hierarquicos:
import scipy
from scipy.cluster.hierarchy import dendrogram, linkage
from scipy.cluster.hierarchy import fcluster
from scipy.cluster.hierarchy import cophenet
from scipy.spatial.distance import pdist

from pylab import rcParams
import seaborn as sb

import sklearn
from sklearn.cluster import AgglomerativeClustering
import sklearn.metrics as sm

import pickle as pkl

# Ler os objetos:
# with open("objetos.pkl", "rb") as f:
#     endereco, \
#     num_de_k_inicial, \
#     K, \
#     WSs_total_otimo_lista, \
#     banco_de_dados, \
#     distancias_otimas, \
#     populacao,\
#     ks_min_otimos = pkl.load(f)

def gerar_grafico_dendrograma(endereco,
                              banco_de_dados,
                              distancias_otimas,
                              k,
                              populacao,
                              titulo_do_eixo_x_do_dendrograma):

    """

    :param endereco: Endereço do banco de dados
    :param banco_de_dados: Banco de dados
    :param distancias_otimas: Distâncias ótimas
    :param k: Número de k-=clusters
    :param populacao: População de
    :param titulo_do_eixo_x_do_dendrograma: Título
    do eixo x do dendrograma
    sementes para exibir no eixo x do dendrograma
    :return: Gráfico dendrograma
    """

    banco_de_dados = pd.DataFrame(banco_de_dados)
    aeronaves = banco_de_dados.iloc[:, 0]

    np.set_printoptions(precision=4, suppress=True)
    plt.figure(figsize=(16, 9.9))
    # plt.style.use("seaborn-whitegrid")
    # plt.style.use("default")

    # teoricos = 24
    # aeronaves = 16
    tamanho_da_letra = 16

    plt.rcParams.update({"text.usetex": True,
                         "text.latex.unicode": True,
                         "font.size": tamanho_da_letra,
                         "font.family": "Book Antiqua",
                         "figure.dpi": 100,
                         "figure.figsize": (6.30, 6.30)})

    # Normalizar os dados
    distancias_otimas = distancias_otimas / np.max(distancias_otimas)

    distancias_otimas = pd.DataFrame(distancias_otimas)
    Y = distancias_otimas.ix[:, 0].values

    # Usando scipy para gerar dendrogramas
    Z = linkage(np.reshape(Y, (len(Y), 1)), "ward")

    n = aeronaves.shape[0]
    aeronaves = list(aeronaves)

    fig = dendrogram(Z,
               p = populacao,
               truncate_mode="lastp",
               leaf_rotation=90,
               leaf_font_size=tamanho_da_letra,
               labels=aeronaves,
               orientation="top",
               distance_sort="descending",
               show_contracted=True)

    plt.title(r"\textbf{Dendrograma Para Uma População de }"
              + str(populacao) + r" \bf{e} $ K = $ " + str(k))
    plt.xlabel(titulo_do_eixo_x_do_dendrograma)
    plt.ylabel("Distâncias Ótimas Normalizadas")

    # plt.axhline(y=500) # Inserir uma linha em y = 500 no dendrograma
    # plt.axhline(y=150) # Inserir uma linha em y = 150 no dendrograma

    # Maximizar a imagem
    figManager = plt.get_current_fig_manager()
    figManager.window.showMaximized()

    # plt.show()
    plt.tight_layout()

    endereco = "resultados_computacionais\\dendrograma_" \
               + endereco + str(k) + ".png"
    plt.savefig(endereco)

    # Quando é gerar os dendrogramas para cada população, se a
    # função abaixo NÃO é utilizada, ocorrerá bug. Além disso,
    # a aplicação executa mais rapidamente quando a mesma
    # é utilizada!
    plt.close("all")

# print(gerar_grafico_dendrograma(endereco,
#                               banco_de_dados,
#                               distancias_otimas,
#                               K,
#                               populacao))