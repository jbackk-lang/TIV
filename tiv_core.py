import numpy as np
from typing import Tuple, List

def calculate_tiv(request) -> Tuple[float, List[List[float]], str]:
    """
    Oblicza TIV dla pojedynczego węzła (wersja skalar + tensor v2).
    Zwraca: (tiv_scalar, tiv_tensor, stability)
    """
    # --- TIV v1 (skalar) ---
    N = request.nominal_value
    R = request.risk
    C = request.context
    H = request.history
    alpha_R = request.alpha_R
    alpha_C = request.alpha_C
    alpha_H = request.alpha_H
    tiv_star = request.tiv_star or N  # domyślnie wartość nominalna
    beta = request.beta

    # Reżim A + B
    V_A = N
    V_B = alpha_R * R + alpha_C * C + alpha_H * H
    TIV_raw = V_A + V_B

    # Stabilizacja (FIELDCORE)
    TIV_stable = TIV_raw - beta * (TIV_raw - tiv_star)

    # Ocena stabilności
    if abs(TIV_stable - tiv_star) < 0.05 * tiv_star:
        stability = "stable"
    elif abs(TIV_stable - tiv_star) < 0.2 * tiv_star:
        stability = "tense"
    else:
        stability = "critical"

    # --- TIV v2 (tensor) ---
    dim = 3  # Domyślnie
    I = np.eye(dim)
    tensor_nominal = N * I
    tensor_risk = np.random.randn(dim, dim) * 0.1 * R
    tensor_context = np.random.randn(dim, dim) * 0.1 * C
    tensor_history = np.random.randn(dim, dim) * 0.1 * H
    tensor_info = (alpha_R * tensor_risk + alpha_C * tensor_context + alpha_H * tensor_history)
    tensor_tiv = tensor_nominal + tensor_info

    # Zastosowanie pola stabilizującego (FIELDCORE - uproszczenie)
    tensor_star = tiv_star * I
    tensor_stable = tensor_tiv - beta * (tensor_tiv - tensor_star)

    return float(TIV_stable), tensor_stable.tolist(), stability

def calculate_tiv_tensor(request) -> Tuple[List[List[float]], str]:
    """
    TIV v2 - pełny tensor dla żądanego wymiaru.
    """
    dim = request.dimension
    N = request.nominal_base
    I = np.eye(dim)
    R = np.random.randn(dim, dim) * 0.1
    C = np.random.randn(dim, dim) * 0.1
    H = np.random.randn(dim, dim) * 0.05

    tensor_nominal = N * I
    tensor_info = request.alpha_R * R + request.alpha_C * C + request.alpha_H * H
    tensor_tiv = tensor_nominal + tensor_info

    # Uproszczona ocena na podstawie normy
    norm = np.linalg.norm(tensor_tiv)
    if norm < 1.5:
        stability = "stable"
    elif norm < 2.5:
        stability = "tense"
    else:
        stability = "critical"

    return tensor_tiv.tolist(), stability
