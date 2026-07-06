def flow_update(tiv_value: float, inflow: float, outflow: float, source: float) -> float:
    """
    Prosty krok przepływu TIV w węźle:
    dTIV/dt = inflow - outflow + source
    """
    return tiv_value + inflow - outflow + source
