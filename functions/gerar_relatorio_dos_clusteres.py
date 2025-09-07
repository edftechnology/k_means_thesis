# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd
import os
import pickle as pkl

def gerar_relatorio_dos_clusteres(endereco,
                                  banco_de_dados,
                                  distancias_otimas,
                                  ks_min_otimos,
                                  num_de_k_inicial,
                                  k,
                                  k_large,
                                  num_max_I):
    r"""
    Gera um arquivo Excel e CSV com os resultados dos clusters,
    salvando-os na pasta 'outputs' da raiz do projeto.
    """

    # Normalizar os dados
    distancias_otimas = distancias_otimas / np.max(distancias_otimas)

    # Preparar dados para DataFrame
    dados_df = np.column_stack((distancias_otimas, ks_min_otimos))
    banco_de_dados_df = pd.DataFrame(banco_de_dados)
    elementos_associados = pd.DataFrame(dados_df,
                                        columns=["Distâncias ótimas normalizadas", "Número do cluster"])
    elementos_associados.index = banco_de_dados_df.iloc[:, 0]

    # Ordenar valores
    elementos_associados.sort_values(by=["Número do cluster", "Distâncias ótimas normalizadas"], ascending=[True, True], inplace=True)
    
    # Exibir o DataFrame resultante
    print(elementos_associados)

    # Extrair o nome base do arquivo de entrada do endereco
    nome_base = os.path.splitext(os.path.basename(endereco))[0] + "_de_" + str(num_de_k_inicial) + "_ate_" + str(k_large) + "_clusters_com_" + str(num_max_I) + "_iteracoes"
    nome_base = nome_base.rstrip('_')  # Remove trailing underscore if any

    # Encontrar a raiz do projeto (um nível acima de 'functions')
    this_dir = os.path.abspath(os.path.dirname(__file__))
    project_root = os.path.dirname(this_dir)
    pasta_outputs = os.path.join(project_root, 'outputs')

    # Criação do diretório de saída se não existir
    pasta_base = os.path.join(pasta_outputs, nome_base)
    pasta_base = pasta_base.replace("__", "_")
    if not os.path.exists(pasta_base):
        os.makedirs(pasta_base)

    # Caminho completo do arquivo Excel
    endereco_completo_arquivo_xlsx = os.path.join(
        pasta_base, f"{nome_base}_cluster_de_numero_{k}.xlsx"
    )
    endereco_completo_arquivo_xlsx = endereco_completo_arquivo_xlsx.replace("__", "_")

    # Salvando os dados em um arquivo .xlsx (uma única vez)
    with pd.ExcelWriter(endereco_completo_arquivo_xlsx, engine='xlsxwriter') as pasta_de_trabalho:
        elementos_associados.to_excel(pasta_de_trabalho, sheet_name='Elementos Associados')

    # Caminho completo do arquivo CSV
    endereco_completo_arquivo_csv = endereco_completo_arquivo_xlsx.replace(".xlsx", ".csv")

    # Salvando os dados em um arquivo .csv
    elementos_associados.to_csv(endereco_completo_arquivo_csv, index=False)

# Exemplo de chamada da função:
# gerar_relatorio_dos_clusteres(endereco, banco_de_dados, distancias_otimas, ks_min_otimos, num_de_k_inicial, k, k_large, num_max_I)
