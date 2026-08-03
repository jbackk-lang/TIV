import numpy as np
from typing import Dict, Any, List

def analyze_gsf(request) -> Dict[str, Any]:
    """
    Analiza GSF na podstawie tensora i wskaźników.
    Zwraca ocenę: continuity, model_reduction, tensor_deformation, risk, stability.
    """
    tensor = np.array(request.tensors)
    continuity = request.continuity_score
    overload = request.model_overload

    # 1. TIMDR - ciągłość danych
    if continuity > 0.85:
        continuity_status = "continuous"
    elif continuity > 0.6:
        continuity_status = "partial_break"
    else:
        continuity_status = "major_break"

    # 2. GIA - redukcja modeli
    # Im wyższy overload, tym większa redukcja potrzebna
    reduced = max(0.0, 1.0 - overload * 0.5)  # uproszczona redukcja

    # 3. FIELDCORE - deformacja tensora
    # Miara deformacji: odchylenie od macierzy diagonalnej
    diag = np.diag(np.diag(tensor))
    deform = np.linalg.norm(tensor - diag) / (np.linalg.norm(tensor) + 1e-8)
    tensor_deformation = float(deform)

    # 4. Ryzyko systemowe
    if tensor_deformation > 0.7 and continuity_status != "continuous":
        risk = "critical"
    elif tensor_deformation > 0.4 or continuity_status == "partial_break":
        risk = "elevated"
    else:
        risk = "low"

    # 5. Ocena globalna
    if risk == "critical" and continuity_status == "major_break":
        field_stability = "critical"
    elif risk == "elevated" or continuity_status == "partial_break":
        field_stability = "tense"
    else:
        field_stability = "stable"

    return {
        "continuity_status": continuity_status,
        "model_reduction": float(reduced),
        "tensor_deformation": tensor_deformation,
        "risk_assessment": risk,
        "field_stability": field_stability
    }

def validate_field(tensor: List[List[float]], threshold: float = 0.5) -> str:
    """
    Walidator struktury pola (VALIDATOR z GSF).
    """
    arr = np.array(tensor)
    norm = np.linalg.norm(arr)
    if norm < threshold:
        return "valid"
    elif norm < 2 * threshold:
        return "warning"
    else:
        return "invalid"
