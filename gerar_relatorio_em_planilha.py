import numpy as np
import pandas as pd
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

def gerar_relatorio_em_planilha(endereco,
                                banco_de_dados,
                                distancias_otimas,
                                ks_min_otimos,
                                k):

    """

    :param endereco: Endereço do banco de dados
    :param banco_de_dados: Banco de dados
    :param distancias_otimas: Distâncias ótimas
    :param ks_min_otimos: Arranjo contendo os k-clusters mínimos
    :param k: Número de k-clusters
    :return: Gerar a planilha com os resultados
    """

    # Normalizar os dados
    distancias_otimas = distancias_otimas / np.max(distancias_otimas)

    elementos_associados = \
        np.concatenate((np.round(distancias_otimas, 3), ks_min_otimos), axis=1)
    elementos_associados = pd.DataFrame(elementos_associados)

    banco_de_dados = pd.DataFrame(banco_de_dados)
    aeronaves = banco_de_dados.iloc[:, 0]

    elementos_associados = \
        pd.DataFrame(np.array(elementos_associados),
                                 index=aeronaves,
                                 columns=["Distâncias ótimas normalizadas",
                                          "Próximo de"])
    elementos_associados = \
        elementos_associados.\
            sort_values(by=["Próximo de"],
                        ascending=True)
    print(elementos_associados)

    # Criar um exportador Pandas Excel usando o XlsxWriter
    # como engine
    endereco = "resultados_computacionais\\resultados_computacionais_" \
               + endereco + str(k) +".xlsx"
    pasta_de_trabalho = pd.ExcelWriter(endereco,
                                       engine="xlsxwriter")

    # Converter o DataFrame em um objeto Excel
    elementos_associados.to_excel(pasta_de_trabalho,
                           sheet_name="elementos_associados")

    # Fechar o exportador Pandas Excel e imprimir o arquivo
    # Excel. NÃO esquecer de manter a planilha fechada quando
    # for executar este código
    pasta_de_trabalho.save()

# print(gerar_relatorio_em_planilha(endereco,
#                                 banco_de_dados,
#                                 distancias_otimas,
#                                 ks_min_otimos,
#                                 K))