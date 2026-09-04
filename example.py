"""
example.py — minimalny przykład użycia timdr_token, uruchamialny wprost:

    python example.py

Wystawia token dla "jacek", zapisuje go szyfrowanego (AES-256-GCM) do
tokens.bin obok tego pliku, pokazuje odczyt z powrotem i typowe
operacje. Klucz trzymamy w OSOBNYM pliku (token.key) - to zwykła
praktyka trybu pliku-klucza: gdyby klucz leżał w tym samym miejscu co
zaszyfrowane dane, szyfrowanie nie chroniłoby przed kimś, kto ma
dostęp do całego folderu. Patrz README.md w tym folderze oraz
docstringi w timdr_token/token.py, timdr_token/repos.py i
timdr_token/crypto_lock.py dla pełnego zastrzeżenia, czym to NIE jest
(nie GitHub, nie audytowany system bezpieczeństwa).
"""
from pathlib import Path

from timdr_token import TokenRegistry, crypto_lock, all_repo_names

STORAGE = Path(__file__).parent / "tokens.bin"
KEYFILE = Path(__file__).parent / "token.key"


def _load_or_create_key() -> bytes:
    if KEYFILE.exists():
        return KEYFILE.read_bytes()
    key = crypto_lock.generate_key()
    KEYFILE.write_bytes(key)
    print(f"Wygenerowano nowy klucz: {KEYFILE} (pilnuj tego pliku - bez niego nie odczytasz tokens.bin).")
    return key


def main() -> None:
    key = _load_or_create_key()
    registry = TokenRegistry(STORAGE, key=key)

    token = registry.get_token("jacek")
    if token is None:
        token = registry.issue_token("jacek", initial_balance=100.0)
        print(f"Wystawiono nowy token dla '{token.owner}' (zapisano zaszyfrowany w {STORAGE}).")
    else:
        print(f"Wczytano istniejacy token dla '{token.owner}' z {STORAGE} (odszyfrowano kluczem).")

    print(f"Liczba repo z dostepem: {len(token.permissions)} / {len(all_repo_names())}")
    print(f"Saldo: {token.balance}")
    print(f"Dostep do SYNOPTYK-ARCTIC/models: {token.has_access('SYNOPTYK-ARCTIC', 'models')}")

    # Przyklad: nowe repo dopisane do REPOS pozniej -> odswiez wszystkie tokeny:
    #   registry.sync_full_access_for_all()


if __name__ == "__main__":
    main()
