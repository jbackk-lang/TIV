"""
repos.py — rejestr repozytoriów z ekosystemu TIMDR (Jacek / jbackk-lang) i
przypisanych im "capabilities" (etykiet możliwości).

WAŻNE ZASTRZEŻENIE, ten sam duch co README `Spoleczny-Protokol-Informacyjny`:
te etykiety to WYŁĄCZNIE lokalna kategoryzacja/bookkeeping w Pythonie - NIE
mają żadnego związku z prawdziwymi uprawnieniami GitHub (kto może pushować,
czytać, zarządzać danym repo na github.com). Nie łączą się z żadnym API
GitHuba i niczego tam nie zmieniają. Jeśli chcesz realnej kontroli dostępu
do repo na GitHubie, to osobny temat (uprawnienia organizacji/collaborators
w ustawieniach repo), nie ten moduł.

Lista folderów zweryfikowana bezpośrednio w Twoim połączonym folderze
(C:\\Users\\jback\\Downloads\\a) 2026-08-31 - nie z pamięci/zgadywania.
Capabilities dla repo, których zawartość znam z audytu w ramach frameworku
TIMDR (patrz skill timdr-signal-framework), są dobrane pod realny temat
repo; dla pozostałych (nieaudytowanych w tej sesji) zostawione ogólne
`["read"]` - dopisz dokładniejsze etykiety, kiedy faktycznie poznasz
zawartość danego repo, zamiast zgadywać.
"""
from __future__ import annotations

REPOS: dict[str, list[str]] = {
    # Synoptyk (pogoda) - projekty z tej samej sesji
    "synoptyk-v2.0-main": ["read", "models", "signals"],
    "SYNOPTYK-ARCTIC": ["read", "models", "signals"],

    # Protokół komunikatów (naprawiony dziś w tej samej sesji)
    "Spoleczny-Protokol-Informacyjny": ["read", "encode"],

    # Predykcja/fuzja stanu (rodzina *-Predict, §23-29 frameworku TIMDR)
    "TIMDR-Grid-Monitor": ["read", "predict", "alerts"],
    "TIMDR-EV-Predict": ["read", "predict", "alerts", "fusion"],
    "TIMDR-Industrial-Predict": ["read", "predict", "alerts", "fusion"],
    "TIMDR-Battery-Predict": ["read", "predict", "alerts", "fusion"],
    "TIMDR-Aviation-Diagnostics": ["read", "predict", "alerts"],

    # Sterowanie / projektowanie
    "TIMDR-Robot": ["read", "control", "predict"],
    "TIMDR-Materials-Design": ["read", "design", "predict"],

    # Meta/fuzja
    "TIMDR-META-DYNAMICS": ["read", "meta", "fusion"],
    "fusion-tools": ["read", "fusion"],

    # Kodowanie / sieci neuronowe (KHIPU, §16 frameworku)
    "KHIPU": ["read", "encode"],
    "KHIPU-NEURAL": ["read", "neural"],

    # Bio
    "TIMDR-DNA": ["read", "bio"],
    "TIMDR-Bio-Signals": ["read", "bio"],

    # Fizyka / sygnały specjalistyczne
    "TIMDR-Quantum-Lattice": ["read", "quantum"],
    "TIMDR-Echosonda-3D": ["read", "sonar"],
    "TIMDR-Radar-Module": ["read", "radar"],
    "TIMDR-Earthquake-Core": ["read", "seismic", "predict"],
    "GIA-TIMDR": ["read", "theory", "cosmo"],
    "probabilistic-timdr": ["read", "probability", "cosmo"],

    # Bezpieczeństwo
    "TIMDR-Security-Module": ["read", "security", "alerts"],

    # Finanse
    "analizator-gieldowy": ["read", "finance", "predict"],
    "analizator-gieldowy-2.0": ["read", "finance", "predict"],
    "analizator-gieldowy-v3": ["read", "finance", "predict"],
    "deliverable_timdr_finanse": ["read", "finance", "predict"],
    "TIMDR-Crypto-Graph": ["read", "finance", "anomaly"],

    # Walidacja / testy / stan
    "math-validator-3.0": ["read", "validate"],
    "math-validator-v2.0": ["read", "validate"],
    "universal-state-analyzer": ["read", "anomaly", "state"],
    "TEST-TIMDR": ["read", "test"],

    # Pozostałe - zawartość nie audytowana w tej sesji, etykiety ogólne
    "THE TIMDR Hyperflow Engine": ["read", "hyperflow"],
    "FLIGHT-TRACKING-TIMDR": ["read"],
    "Boundary-Matter-main": ["read"],
    "PC-main": ["read"],
    "PC_TIMDR": ["read"],
    "Al": ["read"],
    "jbackk-lang.github.io": ["read", "docs"],
}


def all_repo_names() -> list[str]:
    return sorted(REPOS)
