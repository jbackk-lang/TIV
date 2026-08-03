from fastapi import FastAPI, HTTPException
from models import (
    TIVRequest, TIVTensorRequest, TIVResponse,
    GSFRequest, GSFResponse
)
from tiv_core import calculate_tiv, calculate_tiv_tensor
from gsf_core import analyze_gsf, validate_field
import numpy as np

app = FastAPI(
    title="TIMDR/GSF API",
    description="Zintegrowane API dla modeli TIV i GSF",
    version="1.0.0"
)

@app.get("/")
async def root():
    return {
        "message": "TIV & GSF API",
        "endpoints": [
            "/tiv/calculate",
            "/tiv/tensor",
            "/gsf/analyze",
            "/gsf/validate",
            "/health"
        ]
    }

@app.get("/health")
async def health():
    return {"status": "ok"}

@app.post("/tiv/calculate", response_model=TIVResponse)
async def tiv_calculate(request: TIVRequest):
    """
    Oblicza TIV (skalar i tensor) dla pojedynczego węzła.
    """
    try:
        scalar, tensor, stability = calculate_tiv(request)
        return TIVResponse(
            tiv_scalar=scalar,
            tiv_tensor=tensor,
            stability=stability
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/tiv/tensor")
async def tiv_tensor(request: TIVTensorRequest):
    """
    Oblicza pełny tensor TIV v2.
    """
    try:
        tensor, stability = calculate_tiv_tensor(request)
        return {
            "tensor": tensor,
            "dimension": request.dimension,
            "stability": stability
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/gsf/analyze", response_model=GSFResponse)
async def gsf_analyze(request: GSFRequest):
    """
    Analizuje pole globalnego systemu finansowego (GSF).
    """
    try:
        result = analyze_gsf(request)
        return GSFResponse(
            continuity_status=result["continuity_status"],
            model_reduction=result["model_reduction"],
            tensor_deformation=result["tensor_deformation"],
            risk_assessment=result["risk_assessment"],
            field_stability=result["field_stability"]
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/gsf/validate")
async def gsf_validate(tensor: list, threshold: float = 0.5):
    """
    Waliduje strukturę tensora (VALIDATOR).
    """
    try:
        status = validate_field(tensor, threshold)
        return {"status": status, "threshold": threshold}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/tiv/example")
async def tiv_example():
    """
    Przykładowe dane dla TIV.
    """
    example = {
        "node_id": 1,
        "nominal_value": 1.0,
        "risk": 0.2,
        "context": 0.15,
        "history": 0.1,
        "alpha_R": 1.0,
        "alpha_C": 0.8,
        "alpha_H": 0.6,
        "beta": 0.1
    }
    return example

@app.get("/gsf/example")
async def gsf_example():
    """
    Przykładowe dane dla GSF.
    """
    # Przykładowy tensor 3x3 (wpływy między sektorami)
    tensor = [
        [0.8, 0.2, 0.1],
        [0.3, 0.7, 0.4],
        [0.1, 0.2, 0.9]
    ]
    return {
        "tensor": tensor,
        "continuity_score": 0.75,
        "model_overload": 0.6
    }
