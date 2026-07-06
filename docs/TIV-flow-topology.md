# Przepływ TIV i topologia TRM

## 2. Topologia TRM

Sieć finansowa modelujemy jako graf:



\[
G = (V, E)
\]



gdzie:
- \(V\) — zbiór węzłów (podmioty, instytucje, adresy),
- \(E\) — zbiór krawędzi (kanały przepływu).

Każdy przepływ TIV jest ścieżką:



\[
\gamma: [0,1] \to V
\]



Topologiczny wpływ przepływu na wartość:



\[
\Delta TIV(\gamma) = \int_0^1 F(\gamma(s), s) \, ds
\]



gdzie \(F\) jest funkcją „tarcia informacyjnego” (koszt, ryzyko, zmiana kontekstu).

## 3. Równanie przepływu TIV

Dla węzła \(x\):



\[
\frac{\partial TIV(x,t)}{\partial t} = \sum_{y \in \mathcal{N}(x)} F_{y \to x}(t) - \sum_{z \in \mathcal{N}(x)} F_{x \to z}(t) + S(x,t)
\]



gdzie:
- \(\mathcal{N}(x)\) — sąsiedztwo węzła \(x\),
- \(F_{y \to x}(t)\) — przepływ z \(y\) do \(x\),
- \(S(x,t)\) — lokalne źródła/pochłaniacze (emisja, destrukcja).
