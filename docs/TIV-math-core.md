# Rdzeń matematyczny TIV

## 1. Dwoistość: reżim A/B

Definiujemy dwa składniki wartości:



\[
V_A(x,t) \quad \text{— wartość nominalna (stabilna)}
\]




\[
V_B(x,t) \quad \text{— wartość informacyjna (dynamiczna)}
\]



Całkowita wartość TIV:



\[
TIV(x,t) = V_A(x,t) + V_B(x,t)
\]



### 1.1. Reżim A



\[
V_A(x,t) = N(x,t)
\]



gdzie \(N(x,t)\) jest klasyczną wartością nominalną (np. jednostki księgowe), ale już osadzoną w węźle \(x\) i czasie \(t\).

### 1.2. Reżim B



\[
V_B(x,t) = f_R(R(x,t)) + f_C(C(x,t)) + f_H(H(x,t))
\]



gdzie:
- \(R(x,t)\) — lokalne ryzyko,
- \(C(x,t)\) — kontekst (otoczenie informacyjne),
- \(H(x,t)\) — historia przepływu,
- \(f_R, f_C, f_H\) — funkcje wagujące.

Przykładowo:



\[
V_B(x,t) = \alpha_R R(x,t) + \alpha_C C(x,t) + \alpha_H H(x,t)
\]



i wtedy:



\[
TIV(x,t) = N(x,t) + \alpha_R R(x,t) + \alpha_C C(x,t) + \alpha_H H(x,t)
\]


