# -*- coding: utf-8 -*-
import json
import os
from typing import Dict, List, Optional

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import MaxNLocator

from .elbow_detection import summarize_elbow, validation_indices

def gerar_grafico_elbow_data(endereco,
                             num_de_k_inicial,
                             k_large,
                             WSs_total_otimo,
                             num_max_I,
                             sementes: Optional[np.ndarray] = None,
                             ks_min_otimos_lista: Optional[List[np.ndarray]] = None) -> Dict[str, int]:
    r"""
    Gera, anota e salva o gráfico Elbow e um relatório objetivo.

    :param endereco: Caminho do dataset de origem (usado no nome de saída).
    :param num_de_k_inicial: k inicial (inteiro).
    :param k_large: k final (inteiro).
    :param WSs_total_otimo: Lista/array com a distorção por k.
    :param num_max_I: Número máximo de iterações do k-means.
    :param sementes: Dados originais (n x p), opcional (para índices).
    :param ks_min_otimos_lista: Lista de rótulos por k (cada um (n, 1)), opcional.
    :returns: Dicionário com os k sugeridos por método.
    """

    plt.close('all')

    # Normalizar os dados (evitar divisão por zero)
    WSs_total_otimo = np.asarray(WSs_total_otimo, dtype=float).ravel()
    max_w = float(np.max(WSs_total_otimo)) or 1.0
    WSs_total_otimo_normalizado = WSs_total_otimo / max_w

    # Vetor de k para o eixo x
    x = np.arange(num_de_k_inicial, k_large + 1, 1)

    # Sugerir k por métodos objetivos (kneedle, corda, etc.)
    sugestoes = summarize_elbow(x, WSs_total_otimo_normalizado)

    # Preparar índices de validação, se dados/rótulos forem fornecidos
    metrics: Dict[str, Dict[int, float]] = {}
    labels_per_k: Dict[int, np.ndarray] = {}
    if sementes is not None and ks_min_otimos_lista is not None:
        for idx, k in enumerate(x):
            # Garantir shape (n,)
            y_pred = np.asarray(ks_min_otimos_lista[idx], dtype=int).ravel()
            labels_per_k[int(k)] = y_pred
        try:
            metrics = validation_indices(np.asarray(sementes, dtype=float), labels_per_k)
        except Exception:
            metrics = {}

    # Gerar o gráfico Elbow (P&B, marcadores distintos)
    [figure, subcharts] = plt.subplots(figsize=(24, 11))
    subcharts.plot(x, WSs_total_otimo_normalizado,
                   color="black", marker="o", linestyle="-")

    # Anotar os valores em cada ponto
    for i, txt in enumerate(WSs_total_otimo_normalizado):
        valor = txt if np.isscalar(txt) else float(txt)
        subcharts.annotate(f"{valor:.2f}", (x[i], valor), size=10)

    # Configuração dos limites, labels e título
    subcharts.set_xlim([0, k_large + 1])
    subcharts.set_xlabel("$ k $")
    subcharts.set_ylabel("$ WS_{Total} $ Normalizado")
    subcharts.set_title(r"Elbow Data Chart")
    subcharts.xaxis.set_major_locator(MaxNLocator(integer=True))

    # Linhas verticais para sugestões (estilos P&B distintos)
    vstyles = {
        "kneedle": ("--", "Kneedle"),
        "chord": (":", "Max. distância à corda"),
        "segmented": ("-.", "Regressão segmentada"),
        "curvature": ((0, (1, 1)), "Máxima curvatura"),
    }
    for key, k_sug in sugestoes.items():
        ls, label = vstyles.get(key, ("--", key))
        subcharts.axvline(k_sug, color="black", linestyle=ls, linewidth=1.0, label=f"{label}: k={k_sug}")
    subcharts.legend(loc="best")

    plt.tight_layout()

    # Encontrar a raiz do projeto (um nível acima de 'functions')
    this_dir = os.path.abspath(os.path.dirname(__file__))
    project_root = os.path.dirname(this_dir)
    pasta_outputs = os.path.join(project_root, 'outputs')

    # Processamento do nome base
    nome_base = os.path.splitext(os.path.basename(endereco))[0].replace("__", "_") + \
        "_de_" + str(num_de_k_inicial) + "_ate_" + str(k_large) + "_clusters_com_" + str(num_max_I) + "_iteracoes"
    nome_base_parts = nome_base.split('_')

    # Remover a última parte se for numérica
    if nome_base_parts[-1].isdigit():
        nome_base = '_'.join(nome_base_parts[:-1])

    # Criação do diretório de saída se não existir
    pasta_base = os.path.join(pasta_outputs, nome_base)
    pasta_base = pasta_base.replace("__", "_")
    if not os.path.exists(pasta_base):
        os.makedirs(pasta_base)

    # Caminho completo do arquivo de saída
    endereco_completo = os.path.join(pasta_base, f"elbow_data_chart_{nome_base}_cluster_de_numero_{k_large}.png")
    endereco_completo = endereco_completo.replace("__", "_")

    # Salvando a figura ajustada
    figure.savefig(endereco_completo, dpi=300, bbox_inches='tight')
    plt.close(figure)

    # Salvar relatório JSON com sugestões e (se houver) métricas
    relatorio = {
        "suggested_k": sugestoes,
        "k_range": [int(x[0]), int(x[-1])],
        "num_max_iterations": int(num_max_I),
        "normalized_wss": [float(v) for v in WSs_total_otimo_normalizado.tolist()],
        "validation": metrics,
    }
    with open(os.path.join(pasta_base, f"elbow_report_{nome_base}.json"), "w", encoding="utf-8") as f:
        json.dump(relatorio, f, ensure_ascii=False, indent=2)

    return sugestoes

# A função pode ser chamada da seguinte forma:
# gerar_grafico_elbow_data(endereco, num_de_k_inicial, k_large, WSs_total_otimo_lista, num_max_I)
