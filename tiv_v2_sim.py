import numpy as np

# -----------------------------
# Parametry modelu
# -----------------------------

N_NODES = 4          # liczba węzłów w sieci
DIM = 3              # wymiar tensora TIV (macierz DIM x DIM)
DT = 0.01            # krok czasowy
STEPS = 1000         # liczba kroków symulacji

# -----------------------------
# Inicjalizacja sieci
# -----------------------------

# Lista węzłów: 0,1,2,3
nodes = list(range(N_NODES))

# Macierz połączeń (TRM) - prosta sieć pełna
# Gamma[i,j] = 1 oznacza połączenie i->j
Gamma = np.ones((N_NODES, N_NODES)) - np.eye(N_NODES)

# -----------------------------
# Inicjalizacja tensora TIV
# -----------------------------

def init_TIV_tensor():
    """
    Inicjalizuje tensor TIV dla jednego węzła jako macierz DIM x DIM.
    Nominalna część: N * I
    Informacyjna część: losowa macierz
    """
    N = 1.0  # nominalna wartość początkowa
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

# TIV dla każdego węzła
TIV = [init_TIV_tensor() for _ in nodes]

# Docelowy tensor równowagi (TIV*)
TIV_star = [np.zeros((DIM, DIM)) for _ in nodes]

# Tensor beta (siła stabilizacji)
beta = [0.1 * np.eye(DIM) for _ in nodes]

# -----------------------------
# Pole GIA (Phi) - interpretacja globalna
# -----------------------------

def Phi(x, t):
    """
    Proste pole GIA: skalarna modulacja + lekka deformacja macierzowa.
    """
    scale = 1.0 + 0.1 * np.sin(0.01 * t + x)
    M = np.eye(DIM) + 0.05 * np.random.randn(DIM, DIM)
    return scale * M

# -----------------------------
# Tensor przepływu (Flow)
# -----------------------------

def compute_flow(TIV_list, Gamma):
    """
    Oblicza tensor przepływu dla każdego węzła:
    Flow[x] = sum_y Gamma[y,x] * TIV[y] - sum_z Gamma[x,z] * TIV[x]
    """
    flows = []
    for x in nodes:
        inflow = np.zeros((DIM, DIM))
        outflow = np.zeros((DIM, DIM))
        for y in nodes:
            if Gamma[y, x] > 0:
                inflow += Gamma[y, x] * TIV_list[y]
        for z in nodes:
            if Gamma[x, z] > 0:
                outflow += Gamma[x, z] * TIV_list[x]
        flows.append(inflow - outflow)
    return flows

# -----------------------------
# FIELDCORE (stabilizacja)
# -----------------------------

def fieldcore_update(TIV_x, TIV_star_x, beta_x):
    """
    dTIV/dt|Sigma = -beta * (TIV - TIV*)
    """
    return -beta_x @ (TIV_x - TIV_star_x)

# -----------------------------
# Główna pętla symulacji
# -----------------------------

def simulate():
    global TIV
    history = []

    for step in range(STEPS):
        t = step * DT

        # Flow (TIMDR)
        flows = compute_flow(TIV, Gamma)

        # Aktualizacja dla każdego węzła
        new_TIV = []
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
            T_next = T + DT * dT
            new_TIV.append(T_next)

        TIV = new_TIV

        # Zapis historii (np. norma Frobeniusa dla każdego węzła)
        norms = [np.linalg.norm(TIV[x]) for x in nodes]
        history.append(norms)

    return history

# -----------------------------
# Uruchomienie symulacji
# -----------------------------

if __name__ == "__main__":
    history = simulate()
    for step, norms in enumerate(history[::100]):  # co 100 kroków
        print(f"Step {step*100}: ", norms)
