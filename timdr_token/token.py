"""
token.py — lokalny obiekt uprawnień ("TIMDR-Token") dla ekosystemu repo
Jacka (jbackk-lang), plus rejestr z zapisem na dysk (JSON), żeby token nie
znikał po zakończeniu skryptu.

CZYM TO JEST: prosty, w pełni czytelny obiekt Pythona (dataclass) +
prosty plik JSON na dysku - "kto ma jakie etykiety możliwości w jakim
repo" plus licznik `balance` (dowolna liczba, do własnego użytku np. jako
budżet obliczeniowy w Twoich skryptach).

CZYM TO **NIE** JEST (uczciwe zastrzeżenie, ten sam duch co README
`Spoleczny-Protokol-Informacyjny`, sekcja "Sprostowanie"):
- To NIE jest uwierzytelnianie ani autoryzacja GitHub - nie loguje się do
  żadnego konta, nie zmienia uprawnień collaboratorów na github.com, nie
  wystawia żadnego realnego "access token" w sensie GitHuba (Personal
  Access Token / OAuth). Jeśli chcesz kontrolować, kto naprawdę może
  czytać/pisać do Twoich repo na GitHubie, to ustawienia repo/organizacji
  na github.com, zupełnie osobny temat.
- Plik na dysku JEST teraz szyfrowany w spoczynku (AES-256-GCM, patrz
  `crypto_lock.py` - ten sam wzorzec co w naprawie Helix-Lock/Helix Pro),
  ale to NIE czyni z tego audytowanego systemu bezpieczeństwa. To wciąż
  Twój własny klucz/hasło, które Ty przechowujesz i którym Ty zarządzasz -
  jeśli ktoś je pozna, przeczyta i zmodyfikuje plik tak samo łatwo, jak
  gdyby wcale nie był szyfrowany. `has_access()` nadal sprawdza tylko
  zawartość odszyfrowanego pliku, nie nic ponad to.
- Token NICZEGO nie blokuje sam z siebie. To zwykły słownik + metoda
  `has_access()` zwracająca True/False - jeśli Twój własny kod (skrypt,
  funkcja) nie sprawdzi jej wyniku PRZED wykonaniem jakiejś operacji, token
  nie ma żadnego efektu. To narzędzie do PORZĄDKOWANIA własnych skryptów
  ("czy ten skrypt powinien w ogóle próbować X w repo Y"), nie strażnik
  bezpieczeństwa.
- `balance`/`consume()` to zwykła liczba zmiennoprzecinkowa, którą Ty sam
  zmniejszasz wywołując `consume()` w swoim kodzie - nic z zewnątrz nie
  nadaje jej wartości ani nie mierzy żadnego prawdziwego zużycia (compute,
  pieniędzy, czasu), dopóki sam tego nie podepniesz.
"""
from __future__ import annotations

import json
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

from .repos import REPOS
from . import crypto_lock


@dataclass
class TIMDRToken:
    owner: str
    balance: float = 0.0
    permissions: dict[str, list[str]] = field(default_factory=dict)
    issued_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    def grant_full_access(self, repos: dict[str, list[str]] | None = None) -> None:
        """Nadaje dostęp do WSZYSTKICH repo aktualnie zdefiniowanych w
        `repos` (domyślnie `timdr_token.repos.REPOS`). To zrzut stanu w
        chwili wywołania - nie "żyje" automatycznie. Kiedy dopiszesz nowe
        repo do `repos.py` ("i późniejsze repo"), wywołaj tę metodę
        PONOWNIE (albo `TokenRegistry.sync_full_access_for_all()` dla
        wszystkich tokenów naraz), żeby token dostał też nowe pozycje -
        patrz test `test_grant_full_access_is_a_snapshot_not_live`."""
        source = repos if repos is not None else REPOS
        for repo, caps in source.items():
            self.permissions[repo] = list(caps)

    def grant_repo(self, repo: str, capabilities: list[str]) -> None:
        """Dodaje/rozszerza uprawnienia dla JEDNEGO repo (nie nadpisuje
        całkowicie - łączy z tym, co już jest, bez duplikatów)."""
        existing = set(self.permissions.get(repo, []))
        existing.update(capabilities)
        self.permissions[repo] = sorted(existing)

    def revoke_repo(self, repo: str) -> None:
        """Usuwa WSZYSTKIE uprawnienia dla danego repo."""
        self.permissions.pop(repo, None)

    def revoke_capability(self, repo: str, capability: str) -> None:
        """Usuwa jedną konkretną etykietę możliwości z danego repo,
        zostawiając pozostałe nietknięte."""
        if repo in self.permissions:
            self.permissions[repo] = [c for c in self.permissions[repo] if c != capability]
            if not self.permissions[repo]:
                del self.permissions[repo]

    def has_access(self, repo: str, capability: str) -> bool:
        return capability in self.permissions.get(repo, [])

    def consume(self, amount: float) -> bool:
        """Zmniejsza `balance` o `amount`, jeśli starczy - patrz
        zastrzeżenie w docstringu modułu: to zwykła arytmetyka, nie
        mierzy niczego realnego samo z siebie."""
        if amount < 0:
            raise ValueError("consume() nie przyjmuje ujemnych kwot - uzyj innej metody do doladowania")
        if self.balance >= amount:
            self.balance -= amount
            return True
        return False

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> "TIMDRToken":
        return cls(
            owner=data["owner"],
            balance=data.get("balance", 0.0),
            permissions=data.get("permissions", {}),
            issued_at=data.get("issued_at", datetime.now(timezone.utc).isoformat()),
        )


class TokenRegistry:
    """Rejestr tokenów z zapisem do pliku (`storage_path`) - bez tego
    każdy token znikałby po zakończeniu skryptu (poprzednia wersja z
    Twojego szkicu trzymała wszystko tylko w pamięci procesu). Plik jest
    domyślnie szyfrowany w spoczynku (AES-256-GCM, patrz crypto_lock.py) -
    podaj dokładnie jedno z `key` (bytes z crypto_lock.generate_key(),
    przechowuj OSOBNO od tego pliku) albo `password` (str - klucz
    wyprowadzany przez scrypt, sól zapisana w nagłówku pliku).

    Jeśli naprawdę chcesz starego zachowania (jawny tekst, bez żadnej
    ochrony) - np. do szybkich testów lokalnych - ustaw jawnie
    `insecure_plaintext=True` zamiast key/password. To świadomy,
    jawny w kodzie wywołującym wyjątek od domyślnego szyfrowania, nie
    cichy fallback."""

    def __init__(
        self,
        storage_path: str | Path,
        *,
        key: bytes | None = None,
        password: str | None = None,
        insecure_plaintext: bool = False,
    ):
        modes_given = sum(x is not None for x in (key, password)) + (1 if insecure_plaintext else 0)
        if modes_given != 1:
            raise ValueError(
                "podaj dokladnie jedno z: key, password, insecure_plaintext=True"
            )
        self.storage_path = Path(storage_path)
        self._key = key
        self._password = password
        self._insecure_plaintext = insecure_plaintext
        self.tokens: dict[str, TIMDRToken] = {}
        if self.storage_path.exists():
            self.load()

    def issue_token(self, owner: str, initial_balance: float = 100.0, full_access: bool = True) -> TIMDRToken:
        token = TIMDRToken(owner=owner, balance=initial_balance)
        if full_access:
            token.grant_full_access()
        self.tokens[owner] = token
        self.save()
        return token

    def get_token(self, owner: str) -> Optional[TIMDRToken]:
        return self.tokens.get(owner)

    def sync_full_access_for_all(self) -> None:
        """Ponownie nadaje pełny dostęp (wg aktualnego `repos.REPOS`)
        KAŻDEMU istniejącemu tokenowi - wywołaj to po dopisaniu nowych
        repo do repos.py, żeby wszyscy dotychczasowi posiadacze tokenu
        dostali też dostęp do nowych pozycji ("i późniejsze repo"),
        zamiast zakładać nowy token od zera."""
        for token in self.tokens.values():
            token.grant_full_access()
        self.save()

    def save(self) -> None:
        self.storage_path.parent.mkdir(parents=True, exist_ok=True)
        data = {owner: t.to_dict() for owner, t in self.tokens.items()}
        payload = json.dumps(data, indent=2, ensure_ascii=False).encode("utf-8")
        if self._insecure_plaintext:
            self.storage_path.write_bytes(payload)
        else:
            blob = crypto_lock.encrypt_bytes(payload, key=self._key, password=self._password)
            self.storage_path.write_bytes(blob)

    def load(self) -> None:
        raw = self.storage_path.read_bytes()
        if self._insecure_plaintext:
            payload = raw
        else:
            payload = crypto_lock.decrypt_bytes(raw, key=self._key, password=self._password)
        data = json.loads(payload.decode("utf-8"))
        self.tokens = {owner: TIMDRToken.from_dict(d) for owner, d in data.items()}
