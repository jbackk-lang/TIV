# TIV
WWW https://github.com/jbackk-lang/jbackk-lang.github.io      
https://doi.org/10.5281/zenodo.21216173

TIMDR Informational Value
# TIV — TIMDR Informational Value

TIV jest walutą zdefiniowaną jako **pakiet informacji o wartości** w systemie TIMDR:

- dwuwarstwowa (reżim A/B),
- zależna od przepływu (TIMDR-flow),
- osadzona w topologii (TRM),
- interpretowana przez GIA,
- stabilizowana przez FIELDCORE.

Formalnie TIV jest funkcją:



\[
TIV = \mathcal{V}(x, t, \Gamma, \Phi, \Sigma)
\]



gdzie:
- \(x\) — pozycja w sieci (węzeł),
- \(t\) — czas,
- \(\Gamma\) — topologia przepływu (TRM),
- \(\Phi\) — pole GIA (interpretacja),
- \(\Sigma\) — pole FIELDCORE (stabilizacja).

## TIV w LaTeX

\documentclass[12pt]{article}
\usepackage{amsmath, amssymb, amsfonts}
\usepackage{geometry}
\geometry{margin=2.2cm}

\title{TIV --- TIMDR Informational Value \\ Formalny Model Matematyczny}
\author{Jacek / TIMDR Core Architecture}
\date{}

\begin{document}
\maketitle

\section*{1. Definicja waluty TIV}

Waluta TIV jest definiowana jako pakiet informacyjny o wartości:


\[
TIV(x,t) = V_A(x,t) + V_B(x,t),
\]


gdzie:
\begin{itemize}
    \item $x$ --- węzeł w topologii TRM,
    \item $t$ --- czas,
    \item $V_A$ --- wartość nominalna (reżim A),
    \item $V_B$ --- wartość informacyjna (reżim B).
\end{itemize}

\section*{2. Reżim A --- wartość nominalna}

Reżim A jest stabilną wartością transakcyjną:


\[
V_A(x,t) = N(x,t),
\]


gdzie $N(x,t)$ jest wartością księgową przypisaną do węzła $x$.

\section*{3. Reżim B --- wartość informacyjna}

Reżim B jest dynamiczną wartością zależną od ryzyka, kontekstu i historii przepływu:


\[
V_B(x,t) = \alpha_R R(x,t) + \alpha_C C(x,t) + \alpha_H H(x,t),
\]


gdzie:
\begin{itemize}
    \item $R(x,t)$ --- lokalne ryzyko,
    \item $C(x,t)$ --- kontekst informacyjny,
    \item $H(x,t)$ --- historia przepływu,
    \item $\alpha_R, \alpha_C, \alpha_H$ --- wagi reżimu B.
\end{itemize}

\section*{4. Topologia TRM}

System finansowy jest grafem:


\[
G = (V, E),
\]


gdzie $V$ jest zbiorem węzłów, a $E$ zbiorem krawędzi.

Przepływ TIV jest ścieżką:


\[
\gamma : [0,1] \to V.
\]



Wpływ topologii na wartość:


\[
\Delta TIV(\gamma) = \int_0^1 F(\gamma(s), s)\, ds,
\]


gdzie $F$ jest funkcją tarcia informacyjnego.

\section*{5. Równanie przepływu TIMDR}

Dynamika wartości w węźle $x$:


\[
\frac{\partial TIV(x,t)}{\partial t}
=
\sum_{y \in \mathcal{N}(x)} F_{y \to x}(t)
-
\sum_{z \in \mathcal{N}(x)} F_{x \to z}(t)
+
S(x,t),
\]


gdzie:
\begin{itemize}
    \item $F_{y \to x}(t)$ --- przepływ z $y$ do $x$,
    \item $S(x,t)$ --- lokalne źródła/pochłaniacze wartości.
\end{itemize}

\section*{6. Pole GIA --- globalna interpretacja}

Pole interpretacyjne:


\[
\Phi : V \times \mathbb{R} \to \mathbb{R}.
\]



Wartość po interpretacji GIA:


\[
TIV_{\Phi}(x,t) = \Phi(x,t) \cdot TIV(x,t).
\]



\section*{7. Pole FIELDCORE --- stabilizacja}

Pole stabilizujące:


\[
\Sigma : V \times \mathbb{R} \to \mathbb{R}.
\]



Wpływ stabilizacji:


\[
\frac{\partial TIV(x,t)}{\partial t}\Big|_{\Sigma}
=
-\beta \left( TIV(x,t) - TIV^\ast(x) \right),
\]


gdzie:
\begin{itemize}
    \item $TIV^\ast(x)$ --- wartość równowagi,
    \item $\beta$ --- siła stabilizacji.
\end{itemize}

\section*{8. Całkowita dynamika TIV}



\[
\frac{\partial TIV(x,t)}{\partial t}
=
\underbrace{\text{flow}(x,t)}_{\text{TIMDR}}
+
\underbrace{\Phi(x,t) \cdot TIV(x,t)}_{\text{GIA}}
+
\underbrace{-\beta (TIV(x,t) - TIV^\ast(x))}_{\text{FIELDCORE}}.
\]



\section*{9. Ostateczna definicja waluty TIV}



\[
TIV(x,t)
=
N(x,t)
+
\alpha_R R(x,t)
+
\alpha_C C(x,t)
+
\alpha_H H(x,t)
\]




\[
\Rightarrow
TIV_{\text{final}}(x,t)
=
\Phi(x,t)\left[
N(x,t)
+
\alpha_R R(x,t)
+
\alpha_C C(x,t)
+
\alpha_H H(x,t)
\right]
-
\beta (TIV(x,t) - TIV^\ast(x)).
\]



\end{document}

## TIV v2
TIV v2 — Tensor Informational Value Model
1. Wprowadzenie do modelu tensorowego
W wersji v1 waluta TIV była skalarem:
•	TIV(x,t)∈R
W wersji v2 przechodzimy do pełnego tensora wartości:
•	TIV(x,t)∈Rn×n
Tensor pozwala modelować:
•	wielowarstwową wartość,
•	kierunkowość przepływu,
•	sprzężenia między węzłami,
•	gradienty topologiczne,
•	lokalne deformacje wartości.
To jest zgodne z TIMDR, TRM i FIELDCORE.
2. Definicja tensora TIV
Tensor wartości:
•	TIV(x,t)=VA(x,t)+VB(x,t)
gdzie:
•	VA — tensor nominalny (diagonalny),
•	VB — tensor informacyjny (pełny).
3. Tensor nominalny (reżim A)
Nominalna wartość jest diagonalna:
•	VA(x,t)=N(x,t)⋅I
gdzie:
•	I — macierz jednostkowa.
To oznacza, że nominalna wartość nie ma kierunkowości.
4. Tensor informacyjny (reżim B)
Dynamiczna wartość jest pełnym tensorem:
VB(x,t)=αRR(x,t)+αCC(x,t)+αHH(x,t)
gdzie:
•	R(x,t) — tensor ryzyka,
•	C(x,t) — tensor kontekstu,
•	H(x,t) — tensor historii przepływu.
Każdy z nich jest macierzą n×n.
5. Tensor przepływu TIMDR
Przepływ między węzłami jest tensorem:
∂TIV(x,t)∂t=∑y∈N(x)Fy→x(t)−∑z∈N(x)Fx→z(t)+S(x,t)
gdzie:
•	Fy→x(t) — tensor przepływu,
•	S(x,t) — tensor źródeł/pochłaniaczy.
6. Tensor topologii TRM
Topologia TRM jest tensorem połączeń:
Γ(x,y)∈Rn×n
Tensor topologiczny wpływa na wartość:
ΔTIV(γ)=∫01F(γ(s),s) ds
7. Tensor GIA (globalna interpretacja)
Pole interpretacyjne jest tensorem:
Φ(x,t)∈Rn×n
Modulacja wartości:
TIVΦ(x,t)=Φ(x,t)⋅TIV(x,t)
8. Tensor FIELDCORE (stabilizacja)
Pole stabilizujące jest tensorem:
Σ(x,t)∈Rn×n
Dynamika stabilizacji:
∂TIV(x,t)∂t∣Σ=−β(TIV(x,t)−TIV∗(x))
gdzie:
•	β — tensor siły stabilizacji,
•	TIV∗(x) — tensor równowagi.
9. Ostateczne równanie tensorowe TIV v2
∂TIV(x,t)∂t=Flow(x,t)+Φ(x,t)⋅TIV(x,t)−β(TIV(x,t)−TIV∗(x))
10. Finalna definicja TIV v2
TIV(x,t)=N(x,t)I+αRR(x,t)+αCC(x,t)+αHH(x,t)
TIVfinal(x,t)=Φ(x,t)[N(x,t)I+αRR(x,t)+αCC(x,t)+αHH(x,t)]−β(TIV(x,t)−TIV∗(x))


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


