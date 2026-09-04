"""timdr_token — lokalny, jawny system "tokenów" (etykiet możliwości +
licznik) dla ekosystemu repo Jacka. Plik na dysku jest szyfrowany w
spoczynku (AES-256-GCM, patrz crypto_lock.py). Patrz zastrzeżenia w
repos.py i token.py: to NIE jest system uprawnień GitHub."""
from .repos import REPOS, all_repo_names
from .token import TIMDRToken, TokenRegistry
from . import crypto_lock

__all__ = ["REPOS", "all_repo_names", "TIMDRToken", "TokenRegistry", "crypto_lock"]
