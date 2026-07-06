def apply_GIA(tiv_value: float, phi: float) -> float:
    """
    GIA: globalna interpretacja — mnożnik kontekstowy.
    """
    return phi * tiv_value


def apply_FIELDCORE(tiv_value: float, tiv_target: float, beta: float) -> float:
    """
    FIELDCORE: stabilizacja — prosty model powrotu do równowagi.
    dTIV/dt|Sigma = -beta * (TIV - TIV*)
    """
    correction = -beta * (tiv_value - tiv_target)
    return tiv_value + correction
