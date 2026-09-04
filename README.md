# TIMDR-Token

Lokalny system "tokenów" (etykiet możliwości + prosty licznik `balance`)
dla ekosystemu repo Jacka (jbackk-lang), z zapisem stanu do pliku
**szyfrowanego w spoczynku** (AES-256-GCM), żeby przetrwał między
uruchomieniami skryptów, obejmował repo dopisywane później, i nie leżał
jawnym tekstem na dysku.

## Ważne zastrzeżenie — czym to NIE jest

Ten sam duch co README `Spoleczny-Protokol-Informacyjny` (sekcja
"Sprostowanie"):

- **To nie jest system uprawnień GitHub.** Nie loguje się do żadnego
  konta, nie zmienia kto może czytać/pushować do repo na github.com, nie
  wystawia prawdziwego "access token" w sensie GitHuba (Personal Access
  Token / OAuth). Rzeczywistą kontrolę dostępu do repo ustawia się w
  ustawieniach repo/organizacji na github.com — to osobny temat.
- **Szyfrowanie pliku to nie to samo co audytowany system bezpieczeństwa.**
  Plik na dysku jest teraz chroniony prawdziwym AES-256-GCM (patrz niżej),
  ale to wciąż Twój własny klucz/hasło — jeśli ktoś je pozna albo ma
  dostęp do pliku klucza, przeczyta/zmieni zawartość tak samo łatwo jak
  bez szyfrowania. `has_access()` sprawdza tylko zawartość odszyfrowanego
  pliku, nic ponad to.
- **Token niczego nie blokuje sam z siebie.** To słownik + metoda
  `has_access()` zwracająca `True`/`False`. Jeśli Twój kod nie sprawdzi
  jej wyniku przed jakąś operacją, token nie ma żadnego efektu — to
  narzędzie do porządkowania własnych skryptów, nie strażnik
  bezpieczeństwa.
- **`balance`/`consume()`** to zwykła liczba, którą Ty sam zmniejszasz w
  swoim kodzie — nic z zewnątrz jej nie nadaje ani nie mierzy.

## Szyfrowanie pliku na dysku

`crypto_lock.py` chroni `tokens.bin` prawdziwym AES-256-GCM (biblioteka
`cryptography`) — ten sam wzorzec co w naprawie repo Helix-Lock
("Helix Pro", patrz `helix_pro_delivery/` dostarczone osobno, bo to
inne repo bez dostępu push). Dwa tryby, wybierasz jeden przy tworzeniu
`TokenRegistry`:

- **`key=`** — 32 losowe bajty z `crypto_lock.generate_key()`,
  przechowywane w OSOBNYM pliku (np. `token.key`) od `tokens.bin`.
  Najsilniejszy wybór, jeśli możesz bezpiecznie trzymać plik klucza
  osobno.
- **`password=`** — hasło wyprowadzające klucz przez scrypt (sól
  zapisana w nagłówku pliku, nie trzeba jej przechowywać osobno, ale
  samo hasło musi być silne).
- **`insecure_plaintext=True`** — jawny, świadomy powrót do starego
  zachowania (goły JSON) — tylko gdy naprawdę wiesz, że tego chcesz
  (np. szybkie testy lokalne).

Bez podania dokładnie jednego z powyższych `TokenRegistry` rzuca
`ValueError` — nie ma cichego domyślnego trybu jawnego tekstu.

## Struktura

```
timdr_token/
    repos.py        — rejestr repo (nazwa -> lista etykiet możliwości)
    token.py         — TIMDRToken (dataclass) + TokenRegistry
    crypto_lock.py    — AES-256-GCM szyfrowanie pliku (keyfile/hasło)
    __init__.py
tests/
    test_token.py    — 27 testów (patrz niżej)
example.py            — uruchamialny przykład (python example.py)
                         generuje token.key przy pierwszym uruchomieniu
```

`repos.py` zawiera 39 nazw folderów zweryfikowanych bezpośrednio w
połączonym folderze `C:\Users\jback\Downloads\a` (2026-08-31, nie z
pamięci). Etykiety możliwości dla repo poznanych w ramach tej sesji
(np. `synoptyk-v2.0-main`, `SYNOPTYK-ARCTIC`,
`Spoleczny-Protokol-Informacyjny`) są dobrane pod ich realny temat; dla
pozostałych, nieaudytowanych repo zostawione ogólne `["read"]` —
dopisz dokładniejsze etykiety, kiedy faktycznie poznasz zawartość
danego repo.

## Użycie

```python
from timdr_token import TokenRegistry, crypto_lock

key = crypto_lock.generate_key()          # przechowaj OSOBNO od tokens.bin
registry = TokenRegistry("tokens.bin", key=key)
token = registry.issue_token("jacek")     # pelny dostep domyslnie

token.has_access("SYNOPTYK-ARCTIC", "models")  # True
token.grant_repo("KHIPU", ["read", "encode"])  # doprecyzuj/rozszerz jedno repo
token.revoke_capability("KHIPU", "encode")     # odbierz jedna etykiete
```

### "I późniejsze repo"

`grant_full_access()` to zrzut stanu `repos.REPOS` w chwili wywołania —
**nie jest "żywy"**. Kiedy dopiszesz nowe repo do `repos.py`, odśwież
dotychczasowe tokeny jedną linią:

```python
registry.sync_full_access_for_all()
```

Test `test_sync_full_access_for_all_adds_new_repo_to_existing_tokens`
sprawdza dokładnie ten scenariusz wprost.

## Testy

```
cd TIMDR-Token
python -m pytest tests/ -q
```

27/27 testów przechodzi (zweryfikowane 2026-08-31): pokrycie repos.py
(spójność z `all_repo_names()`), pełny/częściowy grant, odbieranie
uprawnień, `consume()`/`balance`, round-trip `to_dict`/`from_dict`,
szyfrowany zapis/odczyt przez `TokenRegistry` w obu trybach (klucz i
hasło), scenariusz "nowe repo później", oraz bezpośrednie testy
`crypto_lock.py`: plik na dysku faktycznie nie da się odczytać jako
JSON bez klucza, zły klucz/hasło jest odrzucany, zmanipulowany plik
jest wykrywany (AES-GCM).

## O co chodziło z Ethereum/blockchainem

Rozważaliśmy podłączenie tego pod Ethereum — nie zrobiliśmy tego
świadomie: to lokalny bookkeeping bez żadnej strony trzeciej, której
nie ufasz (cały sens blockchaina to rozproszony konsensus między
wzajemnie nieufającymi stronami — tu go nie ma), a realny koszt
(gas za każdy zapis, portfel z prawdziwym ETH, zarządzanie kluczem
prywatnym) nie dawał żadnej korzyści dla tego, co ten moduł robi.
Zamiast tego: prawdziwe szyfrowanie pliku lokalnie, za darmo, bez
portfela i bez łańcucha — patrz sekcja wyżej.
