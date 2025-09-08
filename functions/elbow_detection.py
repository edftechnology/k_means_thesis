# -*- coding: utf-8 -*-
r"""
Módulo de detecção objetiva do cotovelo.

Ferramentas objetivas para detectar o ponto ideal no Elbow Data Chart e
calcular índices de validação e estabilidade.

Bloco Sphinx de referência:

.. math:: \dfrac{u}{v}

Notas:
  - Kneedle, distância à corda, regressão segmentada e curvatura discreta.
  - Índices Silhouette, Calinski–Harabasz, Davies–Bouldin.
  - Estabilidade por re-inicializações (ARI médio).
"""

from __future__ import annotations

import math
from typing import Dict, Iterable, List, Sequence, Tuple

import numpy as np

try:
    # scikit-learn 0.20 compat
    from sklearn.metrics import (calinski_harabaz_score as calinski_harabasz_score,  # type: ignore  # noqa: E501
                                 davies_bouldin_score, silhouette_score)
except Exception:  # pragma: no cover - fallback for newer versions
    from sklearn.metrics import (calinski_harabasz_score, davies_bouldin_score,
                                 silhouette_score)  # type: ignore


def _normalize_xy(x: Sequence[float], y: Sequence[float]) -> Tuple[np.ndarray, np.ndarray]:
    """
    Normaliza ``x`` e ``y`` para [0, 1].

    :param x: Abcissas.
    :param y: Ordenadas (decrescentes para Elbow típico).
    :returns: Tupla com ``(x_n, y_n)`` normalizados.
    """
    x_arr = np.asarray(x, dtype=float)
    y_arr = np.asarray(y, dtype=float)
    if x_arr.size < 2:
        return x_arr, y_arr
    x_min, x_max = np.min(x_arr), np.max(x_arr)
    y_min, y_max = np.min(y_arr), np.max(y_arr)
    x_n = (x_arr - x_min) / (x_max - x_min) if x_max > x_min else x_arr * 0.0
    y_n = (y_arr - y_min) / (y_max - y_min) if y_max > y_min else y_arr * 0.0
    # Para curvas decrescentes, inverter y para alinhar com Kneedle (opcional)
    return x_n, y_n


def kneedle_k(x: Sequence[float], y: Sequence[float]) -> int:
    r"""
    Kneedle (Satopaa et al.) para curvas decrescentes.

    Implementação prática: normaliza para [0, 1] e maximiza g(x) = y(x) - x.

    :param x: Valores de k.
    :param y: Métrica de distorção (ex.: WCSS/inertia). Deve decrescer com k.
    :returns: k sugerido.
    """
    x_n, y_n = _normalize_xy(x, y)
    g = y_n - x_n
    idx = int(np.argmax(g))
    return int(x[idx])


def chord_distance_k(x: Sequence[float], y: Sequence[float]) -> int:
    r"""
    Máxima distância perpendicular à corda entre o primeiro e último pontos.

    :param x: Valores de k.
    :param y: Métrica de distorção (ex.: WCSS/inertia).
    :returns: k sugerido.
    """
    x_n, y_n = _normalize_xy(x, y)
    # Reta (x0, y0) -> (x1, y1)
    x0, y0 = x_n[0], y_n[0]
    x1, y1 = x_n[-1], y_n[-1]
    dx, dy = x1 - x0, y1 - y0
    denom = math.hypot(dx, dy) or 1.0
    # Distância perpendicular ponto-reta
    d = np.abs(dy * x_n - dx * y_n + x1 * y0 - y1 * x0) / denom
    idx = int(np.argmax(d))
    return int(x[idx])


def segmented_regression_k(x: Sequence[float], y: Sequence[float]) -> int:
    r"""
    Regressão segmentada (duas retas) via busca exaustiva no breakpoint.

    Minimiza o erro quadrático total ao ajustar duas retas (OLS) em
    ``[x_min, k*]`` e ``[k*, x_max]``.

    :param x: Valores de k.
    :param y: Métrica de distorção (ex.: WCSS/inertia).
    :returns: k sugerido.
    """
    x_arr = np.asarray(x, dtype=float)
    y_arr = np.asarray(y, dtype=float)
    n = x_arr.size
    if n < 3:
        return int(x_arr[0])

    def fit_line(xv: np.ndarray, yv: np.ndarray) -> Tuple[float, float]:
        # y = a*x + b via OLS
        A = np.vstack([xv, np.ones_like(xv)]).T
        sol, _, _, _ = np.linalg.lstsq(A, yv, rcond=None)
        a, b = float(sol[0]), float(sol[1])
        return a, b

    best_k = int(x_arr[1])
    best_err = float("inf")
    # Evitar extremos como breakpoint
    for i in range(1, n - 1):
        a1, b1 = fit_line(x_arr[:i + 1], y_arr[:i + 1])
        a2, b2 = fit_line(x_arr[i:], y_arr[i:])
        y1_hat = a1 * x_arr[:i + 1] + b1
        y2_hat = a2 * x_arr[i:] + b2
        err = float(np.sum((y_arr[:i + 1] - y1_hat) ** 2) + np.sum((y_arr[i:] - y2_hat) ** 2))
        if err < best_err:
            best_err = err
            best_k = int(x_arr[i])
    return best_k


def discrete_curvature_k(x: Sequence[float], y: Sequence[float]) -> int:
    r"""
    Seleciona o k de máxima curvatura discreta via três pontos consecutivos.

    :param x: Valores de k.
    :param y: Métrica de distorção (ex.: WCSS/inertia).
    :returns: k sugerido.
    """
    x_arr = np.asarray(x, dtype=float)
    y_arr = np.asarray(y, dtype=float)
    if x_arr.size < 3:
        return int(x_arr[0])
    # Curvatura via ângulo entre vetores (p_{i-1}->p_i) e (p_i->p_{i+1})
    angs: List[float] = []
    for i in range(1, len(x_arr) - 1):
        v1 = np.array([x_arr[i] - x_arr[i - 1], y_arr[i] - y_arr[i - 1]], dtype=float)
        v2 = np.array([x_arr[i + 1] - x_arr[i], y_arr[i + 1] - y_arr[i]], dtype=float)
        # Evitar divisões por zero
        n1 = np.linalg.norm(v1) or 1.0
        n2 = np.linalg.norm(v2) or 1.0
        cosang = float(np.clip(np.dot(v1, v2) / (n1 * n2), -1.0, 1.0))
        ang = math.acos(cosang)
        angs.append(ang)
    idx = int(np.argmax(angs)) + 1
    return int(x_arr[idx])


def summarize_elbow(x: Sequence[float], y: Sequence[float]) -> Dict[str, int]:
    """
    Resume os detectores de cotovelo em um único dicionário.

    :returns: dict com chaves: ``kneedle``, ``chord``, ``segmented``, ``curvature``.
    """
    return {
        "kneedle": kneedle_k(x, y),
        "chord": chord_distance_k(x, y),
        "segmented": segmented_regression_k(x, y),
        "curvature": discrete_curvature_k(x, y),
    }


def validation_indices(
    data: np.ndarray,
    labels_per_k: Dict[int, np.ndarray],
) -> Dict[str, Dict[int, float]]:
    r"""
    Calcula Silhouette, Calinski–Harabasz e Davies–Bouldin por k.

    :param data: Matriz de dados (n x p).
    :param labels_per_k: Dicionário {k: labels (n,)}.
    :returns: Dicionário de métricas por nome e k.
    """
    metrics: Dict[str, Dict[int, float]] = {"silhouette": {}, "calinski_harabasz": {}, "davies_bouldin": {}}
    for k, y_pred in labels_per_k.items():
        # Requer ao menos 2 clusters e menos que n amostras
        if k < 2 or k >= data.shape[0]:
            continue
        try:
            metrics["silhouette"][k] = float(silhouette_score(data, y_pred))
        except Exception:
            metrics["silhouette"][k] = float("nan")
        try:
            # Compatibilidade de nome
            try:
                ch = float(calinski_harabasz_score(data, y_pred))  # type: ignore
            except Exception:
                ch = float(calinski_harabasz_score(data, y_pred))  # noqa
            metrics["calinski_harabasz"][k] = ch
        except Exception:
            metrics["calinski_harabasz"][k] = float("nan")
        try:
            metrics["davies_bouldin"][k] = float(davies_bouldin_score(data, y_pred))
        except Exception:
            metrics["davies_bouldin"][k] = float("nan")
    return metrics


def stability_by_restarts(
    data: np.ndarray,
    k_values: Iterable[int],
    num_max_I: int,
    run_kmeans,
    n_repeats: int = 10,
    random_states: Sequence[int] | None = None,
) -> Dict[int, float]:
    r"""
    Estabilidade via re-inicializações no conjunto completo (sem reamostragem).

    Mede a média do ARI entre todas as combinações de reinicializações por k.
    Usa uma função ``run_kmeans`` compatível com ``functions.k_means.k_means``.

    :param data: Matriz de dados (n x p).
    :param k_values: Conjunto de k a avaliar.
    :param num_max_I: Número máximo de iterações por execução do k-means.
    :param run_kmeans: Função que recebe (k, data, num_max_I) e retorna labels (n,).
    :param n_repeats: Número de repetições por k.
    :param random_states: Sementes para reprodutibilidade (opcional).
    :returns: Dicionário {k: estabilidade_ARI_médio}.
    """
    from sklearn.metrics import adjusted_rand_score as ari

    n = data.shape[0]
    rs = list(random_states) if random_states is not None else list(range(1234, 1234 + n_repeats))
    scores: Dict[int, float] = {}
    for k in k_values:
        if k < 2 or k >= n:
            continue
        labels_runs: List[np.ndarray] = []
        for i in range(n_repeats):
            # Controlar PRNG para reprodutibilidade leve
            np.random.seed(rs[i % len(rs)])
            y_pred = run_kmeans(k, data, num_max_I)
            labels_runs.append(np.asarray(y_pred, dtype=int).ravel())
        # ARI médio entre todas as combinações
        if len(labels_runs) < 2:
            scores[k] = float("nan")
            continue
        vals: List[float] = []
        for i in range(len(labels_runs)):
            for j in range(i + 1, len(labels_runs)):
                vals.append(float(ari(labels_runs[i], labels_runs[j])))
        scores[k] = float(np.mean(vals)) if vals else float("nan")
    return scores
