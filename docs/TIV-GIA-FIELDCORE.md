# GIA i FIELDCORE w wycenie TIV

## 4. Pole GIA — interpretacja globalna

Definiujemy pole interpretacyjne:



\[
\Phi: V \times \mathbb{R} \to \mathbb{R}
\]



które modyfikuje wartość:



\[
TIV_\Phi(x,t) = \Phi(x,t) \cdot TIV(x,t)
\]



\(\Phi\) uwzględnia globalny kontekst (makro, systemowe ryzyko, globalne przepływy).

## 5. Pole FIELDCORE — stabilizacja

Definiujemy pole stabilizujące:



\[
\Sigma: V \times \mathbb{R} \to \mathbb{R}
\]



które działa jako korektor:



\[
\frac{\partial TIV(x,t)}{\partial t} \Big|_{\Sigma} = - \beta \left( TIV(x,t) - TIV^\ast(x) \right)
\]



gdzie:
- \(TIV^\ast(x)\) — docelowy poziom równowagi,
- \(\beta\) — współczynnik siły stabilizacji.

Całkowita dynamika:



\[
\frac{\partial TIV(x,t)}{\partial t} = \text{flow}(x,t) + \text{GIA}(x,t) + \text{FIELDCORE}(x,t)
\]


