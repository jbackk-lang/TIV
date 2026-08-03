from pydantic import BaseModel
from typing import List, Optional, Dict, Any

class TIVRequest(BaseModel):
    node_id: int                      # ID węzła
    nominal_value: float = 1.0        # N (wartość nominalna)
    risk: float = 0.1                 # R (ryzyko)
    context: float = 0.1              # C (kontekst)
    history: float = 0.05             # H (historia)
    alpha_R: float = 1.0
    alpha_C: float = 1.0
    alpha_H: float = 0.5
    tiv_star: Optional[float] = 1.0   # Wartość równowagi
    beta: float = 0.1                 # Siła stabilizacji

class GSFRequest(BaseModel):
    tensors: List[List[float]]        # Tensor wpływu (np. między sektorami)
    continuity_score: float = 0.8     # Ocena ciągłości danych (TIMDR)
    model_overload: float = 0.7       # Nadmiar modeli (GIA)

class TIVTensorRequest(BaseModel):
    node_id: int
    dimension: int = 3                # Dla TIV v2 (tensor DIM x DIM)
    nominal_base: float = 1.0
    alpha_R: float = 1.0
    alpha_C: float = 1.0
    alpha_H: float = 0.5

class TIVResponse(BaseModel):
    tiv_scalar: float
    tiv_tensor: List[List[float]]
    stability: str                    # "stable", "tense", "critical"

class GSFResponse(BaseModel):
    continuity_status: str
    model_reduction: float
    tensor_deformation: float
    risk_assessment: str
    field_stability: str
