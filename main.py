# coding: utf-8
"""
Fundação Universidade Federal do ABC

Trabalho de Graduação em Engenharia III

Data de Criação: 06/03/2018
Data da última modificação: 28/09/2018
"""
# REVISÃO(ÕES): --------

# REFERÊNCIA(S): -------------------------------------------------------------------------------------------------------

# [1] MacQueen.
# [2] Ricieri
# [3] Livros de Python

# FUNÇÃO DO APLICATIVO: ------------------------------------------------------------------------------------------------

# Função: classificar.

# PACOTE(S): -----------------------------------------------------------------------------------------------------------

import time as time
import numpy as np
import pandas as pd
import os as os
import pickle as pkl
import validacoes_das_variaveis as vv
import k_means as km
import gerar_grafico_elbow_data as ed
import gerar_relatorio_em_planilha as re
import gerar_grafico_dendrograma as de
import winsound as winsound

# CARREGAMENTO, ARMAZENAMENTO E MANIPULAÇÃO DO DADOS: ------------------------------------------------------------------

# endereco = "banco_de_dados\\tres_ponto_um.xlsx"
# endereco = "banco_de_dados\\quatro_ponto_um.xlsx"
# endereco = "banco_de_dados\\seis_ponto_um.xlsx"
# endereco = "banco_de_dados\\aeronaves_civis.xlsx"
# endereco = "banco_de_dados\\aeronaves_civis_arbitrado.xlsx"
# endereco = "banco_de_dados\\aeronaves_militares.xlsx"
# endereco = "banco_de_dados\\aeronaves_militares_arbitrado.xlsx"
# endereco = "banco_de_dados\\turbinas_60_licoes.xlsx"
# endereco = "banco_de_dados\\foguetes.xlsx"
endereco = "banco_de_dados\\OS9216_18032020-A_alterado.xlsm"

endereco =  "banco_de_dados/hubglobe.xlsx"


banco_de_dados = pd.read_excel(endereco,
                               sheet_name=0)

bd_auxiliar = banco_de_dados

bd_auxiliar.columns = \
    bd_auxiliar.columns.str.replace(" ", "_")
bd_auxiliar.columns = \
    bd_auxiliar.columns.str.replace("-", "_")
bd_auxiliar.columns = \
    bd_auxiliar.columns.str.replace("__", "_")
# print(bd_auxiliar.head())

# A primeira coluna é removida, pois trata-se do "Nome da Aeronave"
bd_auxiliar = \
    bd_auxiliar.drop(bd_auxiliar.columns[0], axis = 1)
# A primeira coluna é removida, pois trata-se da
# "Data de Entrada de Operação"
# bd_auxiliar = \
#     bd_auxiliar.drop(bd_auxiliar.columns[0], axis = 1)
print(bd_auxiliar.head())

print(bd_auxiliar.shape)

# VARIÁVEL(IS): --------------------------------------------------------------------------------------------------------

print("-----------")
print("VARIÁVEL(IS):")
print("")

# sementes = Sementes do BIG Data
sementes = bd_auxiliar.values

# n = Número total de elementos
n = sementes.shape[0]

# num_de_variaveis = Número de variáveis
num_de_variaveis = sementes.shape[1]

# print(sementes)
# print(sementes.shape)

# digitar k-clusters;
# K = Número total de clusters
K = input("Digitar o 'Número de total de k-clusters' = ")
descricao = "Número de total k-clusters"
K = vv.validar_variavel_inteira_nao_negativa(K, descricao)
# Condição para não gerar mais grupos do que elementos
porcentagem = 0.80
if K >= porcentagem * n:
    print("Espeficique um valor de "
          "'Número Total K de k-clusters' menor que",
          int(porcentagem * n))
    quit()
print("Número total K de k-clusters =", K)

# num_max_I = Número máximo de iterações
num_max_I = input("Digitar o 'Número total de iterações' = ")
descricao = "Número total de iterações"
num_max_I = \
    vv.validar_variavel_inteira_nao_negativa(num_max_I, descricao)
print("Número máximo de iterações =", num_max_I)

num_de_k_inicial = input("Digitar o 'Número do k Inicial' = ")
descricao = "Número do k Inicial"
num_de_k_inicial = \
    vv.validar_variavel_inteira_nao_negativa(num_de_k_inicial, descricao)
if num_de_k_inicial <= 1 or num_de_k_inicial > K:
    print("Espeficique um valor de "
          "'Número do k Inicial' maior que 1 (um)"
          "e menor que o 'Número Total K de k-clusters'.")
    quit()
print("Número do k Inicial =", num_de_k_inicial)

titulo_do_eixo_x_do_dendrograma = input("Digitar o "
                                        "'Título do Eixo x do Dendrograma': ")

# CÁLCULO(S): ----------------------------------------------------------------------------------------------------------

tempo_inicio = time.time()
tempo_inicio_CPU = time.clock()

# os medioides_otimos devem ser um arranjo
medioides_otimos_lista = []
ks_min_otimos_lista = []
WSs_total_otimo_lista = []

for k in range(num_de_k_inicial, K + 1, 1):
    distancias_otimas, medioides_otimos, \
    ks_min_otimos, WS_total_otimo = \
        km.k_means(num_de_k_inicial, k, sementes, num_max_I)
    medioides_otimos_lista.append(medioides_otimos)
    ks_min_otimos_lista.append(ks_min_otimos)
    WSs_total_otimo_lista.append(WS_total_otimo)

    print("k_atual = ", k)

# RESULTADO(S): --------------------------------------------------------------------------------------------------------

    print("----------")
    print("RESULTADO(S) PARA k =", k, ":")
    print("")

    print("Medioides ótimos:")
    print(medioides_otimos_lista)
    print("")

    # Gerar relatório em planilha:
    endereco = endereco.replace("banco_de_dados\\", "")
    endereco = endereco.replace(".xlsx", "_")
    re.gerar_relatorio_em_planilha(endereco,
                                   banco_de_dados,
                                   distancias_otimas,
                                   ks_min_otimos,
                                   k)

    print("")
    print("WS total ótimo:")
    print(WSs_total_otimo_lista)
    print("")

    # Gráfico(s):

    # Plotar Dendrograma:
    if n <= 40:
        populacao = n
    else:
        populacao = 40

    # for populacao in range(2, n + 1, 1): Caso se queira executar
    # o programa para gerar is elbow data charts para cada valor
    # de população

    endereco_antigo = endereco
    endereco = endereco + str(populacao) + "_"

    de.gerar_grafico_dendrograma(endereco,
                                 banco_de_dados,
                                 distancias_otimas,
                                 k,
                                 populacao,
                                 titulo_do_eixo_x_do_dendrograma)

    endereco = endereco_antigo

# Plotar o Elbow Data Chart:

endereco = endereco.replace("banco_de_dados\\", "")
endereco = endereco + str(n) + "_"

ed.gerar_grafico_elbow_data(endereco,
                            num_de_k_inicial,
                            K,
                            WSs_total_otimo_lista)

frequencia = 2500 # (Hertz)
duracao = 1000 # (ms)
winsound.Beep(frequencia, duracao)

tempo_fim = time.time() - tempo_inicio
tempo_fim_CPU = time.clock() - tempo_inicio_CPU
print("----------")
print("O tempo de execução da aplicação é =",
      round(tempo_fim, 2), "s")

# Os objetos estão sendo salvos para NÃO ter que executar
# todo o código novamente, simplemente para executar
# a function abaixo
# Salvar os objetos:
with open("objetos.pkl", "wb") as f:
    pkl.dump([endereco,
              num_de_k_inicial,
              K,
              WSs_total_otimo_lista,
              banco_de_dados,
              distancias_otimas,
              populacao,
              ks_min_otimos],
             f)