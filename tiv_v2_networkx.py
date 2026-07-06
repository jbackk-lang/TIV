import numpy as np
import networkx as nx

# ---------------------------------------------------------
# PARAMETRY
# ---------------------------------------------------------

DIM = 3          # wymiar tensora TIV (macierz DIM x DIM)
DT = 0.01        # krok czasowy
STEPS = 2000     # liczba kroków symulacji

# ---------------------------------------------------------
# TWORZENIE PRAWDZIWEGO GRAFU NETWORKX
# ---------------------------------------------------------

# Przykład: graf finansowy z różnymi wagami przepływów
G = nx.DiGraph()

# Dodajemy węzły (banki, instytucje, kraje)
G.add_nodes_from([0, 1, 2, 3, 4])

# Dodajemy krawędzie z wagami (siła połączenia finansowego)
edges = [
    (0, 1, 0.8),
    (1, 2, 0.5),
    (2, 3, 0.9),
    (3, 4, 0.4),
    (4, 0, 0.7),
    (1, 3, 0.6),
    (0, 2, 0.3)
]

for u, v, w in edges:
    G.add_edge(u, v, weight=w)

nodes = list(G.nodes)

# ---------------------------------------------------------
# INICJALIZACJA TENSORA TIV
# ---------------------------------------------------------

def init_TIV_tensor():
    N = 1.0
    I = np.eye(DIM)

    R = np.random.randn(DIM, DIM) * 0.1
    C = np.random.randn(DIM, DIM) * 0.1
    H = np.zeros((DIM, DIM))

    alpha_R = 1.0
    alpha_C = 1.0
    alpha_H = 0.5

    V_A = N * I
    V_B = alpha_R * R + alpha_C * C + alpha_H * H

    return V_A + V_B

TIV = {x: init_TIV_tensor() for x in nodes}

# Tensor równowagi
TIV_star = {x: np.zeros((DIM, DIM)) for x in nodes}

# Tensor beta
beta = {x: 0.1 * np.eye(DIM) for x in nodes}

# ---------------------------------------------------------
# GIA — GLOBAL INTERPRETATION FIELD
# ---------------------------------------------------------

def Phi(x, t):
    scale = 1.0 + 0.1 * np.sin(0.01 * t + x)
    M = np.eye(DIM) + 0.05 * np.random.randn(DIM, DIM)
    return scale * M

# ---------------------------------------------------------
# FLOW — PRZEPŁYW TENSOROWY PO GRAFIE
# ---------------------------------------------------------

def compute_flow(TIV_dict):
    flows = {x: np.zeros((DIM, DIM)) for x in nodes}

    for u, v, data in G.edges(data=True):
        w = data["weight"]
        flows[v] += w * TIV_dict[u]      # dopływ
        flows[u] -= w * TIV_dict[u]      # odpływ

    return flows

# ---------------------------------------------------------
# FIELDCORE — STABILIZACJA
# ---------------------------------------------------------

def fieldcore_update(TIV_x, TIV_star_x, beta_x):
    return -beta_x @ (TIV_x - TIV_star_x)

# ---------------------------------------------------------
# SYMULACJA
# ---------------------------------------------------------

def simulate():
    global TIV
    history = []

    for step in range(STEPS):
        t = step * DT

        flows = compute_flow(TIV)

        new_TIV = {}

        for x in nodes:
            T = TIV[x]

            # GIA
            Phi_x = Phi(x, t)
            gia_term = Phi_x @ T

            # FIELDCORE
            fc_term = fieldcore_update(T, TIV_star[x], beta[x])

            # Całkowita zmiana
            dT = flows[x] + gia_term + fc_term

            # Euler step
            new_TIV[x] = T + DT * dT

        TIV = new_TIV

        # Normy Frobeniusa dla każdego węzła
        norms = {x: np.linalg.norm(TIV[x]) for x in nodes}
        history.append(norms)

    return history

# ---------------------------------------------------------
# URUCHOMIENIE
# ---------------------------------------------------------

if __name__ == "__main__":
    history = simulate()

    print("Co 200 kroków:")
    for i in range(0, len(history), 200):
        print(f"Step {i}: {history[i]}")
