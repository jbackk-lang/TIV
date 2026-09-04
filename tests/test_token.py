"""
test_token.py — testy dla timdr_token (repos.py + token.py + crypto_lock.py).
Sprawdzają głównie: (a) że pełny dostęp faktycznie odzwierciedla aktualny
REPOS, (b) że grant_full_access() to zrzut stanu, nie coś "żywego"
(kluczowe rozróżnienie z docstringu, warte testu wprost, nie tylko
opisu), (c) że zapis/odczyt (teraz szyfrowany) daje dokładnie ten sam
stan tokenu, (d) drobne operacje na uprawnieniach (grant/revoke) i na
balance, (e) że plik na dysku faktycznie NIE jest już czytelnym
tekstem, i że zły klucz/hasło jest odrzucany.
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import pytest

from timdr_token.repos import REPOS, all_repo_names
from timdr_token.token import TIMDRToken, TokenRegistry
from timdr_token import crypto_lock
from timdr_token.crypto_lock import CryptoLockError


def test_all_repo_names_matches_repos_keys():
    assert all_repo_names() == sorted(REPOS)


def test_grant_full_access_covers_every_repo_in_registry():
    token = TIMDRToken(owner="jacek")
    token.grant_full_access()
    assert set(token.permissions) == set(REPOS)
    for repo, caps in REPOS.items():
        assert token.permissions[repo] == list(caps)


def test_grant_full_access_is_a_snapshot_not_live():
    """Kluczowe rozroznienie z docstringu grant_full_access(): dopisanie
    nowego repo do slownika PO wywolaniu grant_full_access() nie pojawia
    sie automatycznie w uprawnieniach tokenu - trzeba wywolac ja ponownie
    (albo sync_full_access_for_all() w rejestrze)."""
    local_repos = dict(REPOS)
    token = TIMDRToken(owner="jacek")
    token.grant_full_access(repos=local_repos)
    assert "Nowe-Repo-Z-Przyszlosci" not in token.permissions

    local_repos["Nowe-Repo-Z-Przyszlosci"] = ["read"]
    assert "Nowe-Repo-Z-Przyszlosci" not in token.permissions

    token.grant_full_access(repos=local_repos)
    assert token.has_access("Nowe-Repo-Z-Przyszlosci", "read")


def test_has_access_true_and_false():
    token = TIMDRToken(owner="jacek")
    token.grant_repo("SYNOPTYK-ARCTIC", ["read", "models"])
    assert token.has_access("SYNOPTYK-ARCTIC", "read")
    assert not token.has_access("SYNOPTYK-ARCTIC", "delete")
    assert not token.has_access("Nieistniejace-Repo", "read")


def test_grant_repo_merges_without_duplicates():
    token = TIMDRToken(owner="jacek")
    token.grant_repo("KHIPU", ["read"])
    token.grant_repo("KHIPU", ["read", "encode"])
    assert token.permissions["KHIPU"] == ["encode", "read"]


def test_revoke_repo_removes_all_capabilities():
    token = TIMDRToken(owner="jacek")
    token.grant_repo("KHIPU", ["read", "encode"])
    token.revoke_repo("KHIPU")
    assert "KHIPU" not in token.permissions
    assert not token.has_access("KHIPU", "read")


def test_revoke_capability_keeps_other_capabilities():
    token = TIMDRToken(owner="jacek")
    token.grant_repo("KHIPU", ["read", "encode"])
    token.revoke_capability("KHIPU", "encode")
    assert token.has_access("KHIPU", "read")
    assert not token.has_access("KHIPU", "encode")


def test_revoke_last_capability_removes_repo_entry_entirely():
    token = TIMDRToken(owner="jacek")
    token.grant_repo("KHIPU", ["read"])
    token.revoke_capability("KHIPU", "read")
    assert "KHIPU" not in token.permissions


def test_consume_succeeds_when_balance_sufficient():
    token = TIMDRToken(owner="jacek", balance=10.0)
    assert token.consume(4.0) is True
    assert token.balance == 6.0


def test_consume_fails_when_balance_insufficient():
    token = TIMDRToken(owner="jacek", balance=1.0)
    assert token.consume(5.0) is False
    assert token.balance == 1.0


def test_consume_rejects_negative_amount():
    token = TIMDRToken(owner="jacek", balance=10.0)
    with pytest.raises(ValueError):
        token.consume(-1.0)


def test_to_dict_from_dict_roundtrip():
    token = TIMDRToken(owner="jacek", balance=42.0)
    token.grant_repo("KHIPU", ["read", "encode"])
    restored = TIMDRToken.from_dict(token.to_dict())
    assert restored == token


def test_registry_issue_token_grants_full_access_by_default():
    registry = TokenRegistry.__new__(TokenRegistry)  # unikamy zapisu na dysk w tym tescie
    registry.storage_path = None
    registry.tokens = {}
    registry._insecure_plaintext = True
    registry.save = lambda: None  # noqa: E731 - podmiana zapisu na no-op tylko na potrzeby tego testu
    token = registry.issue_token("jacek")
    assert set(token.permissions) == set(REPOS)
    assert token.balance == 100.0


def test_registry_get_token_returns_none_for_unknown_owner():
    registry = TokenRegistry.__new__(TokenRegistry)
    registry.storage_path = None
    registry.tokens = {}
    registry._insecure_plaintext = True
    assert registry.get_token("nieznany") is None


def test_registry_requires_exactly_one_key_source():
    with pytest.raises(ValueError):
        TokenRegistry("/tmp/nieistotne.tokens")
    with pytest.raises(ValueError):
        TokenRegistry("/tmp/nieistotne.tokens", key=crypto_lock.generate_key(), insecure_plaintext=True)


def test_registry_save_and_load_roundtrip_key_mode(tmp_path):
    path = tmp_path / "tokens.bin"
    key = crypto_lock.generate_key()
    registry = TokenRegistry(path, key=key)
    token = registry.issue_token("jacek", initial_balance=5.0)
    token.grant_repo("KHIPU", ["read"])
    registry.save()

    reloaded = TokenRegistry(path, key=key)
    reloaded_token = reloaded.get_token("jacek")
    assert reloaded_token is not None
    assert reloaded_token.balance == 5.0
    assert reloaded_token.has_access("KHIPU", "read")
    assert set(reloaded_token.permissions) == set(REPOS)


def test_registry_save_and_load_roundtrip_password_mode(tmp_path):
    path = tmp_path / "tokens.bin"
    registry = TokenRegistry(path, password="bardzo-tajne-haslo")
    registry.issue_token("jacek", initial_balance=7.0)

    reloaded = TokenRegistry(path, password="bardzo-tajne-haslo")
    assert reloaded.get_token("jacek").balance == 7.0


def test_registry_file_on_disk_is_not_readable_plaintext(tmp_path):
    """Sedno prosby uzytkownika: plik nie moze lezec jawnie. Zapisujemy
    token z rozpoznawalna nazwa wlasciciela i sprawdzamy, ze surowe bajty
    pliku NIE zawieraja tej nazwy ani zadnego fragmentu JSON-a."""
    path = tmp_path / "tokens.bin"
    key = crypto_lock.generate_key()
    registry = TokenRegistry(path, key=key)
    registry.issue_token("rozpoznawalny-wlasciciel-XYZ")

    raw = path.read_bytes()
    assert b"rozpoznawalny-wlasciciel-XYZ" not in raw
    assert b"permissions" not in raw
    assert raw.startswith(crypto_lock.MAGIC)  # naglowek szyfrowania, nie JSON
    import json as _json
    import pytest as _pytest
    with _pytest.raises((_json.JSONDecodeError, UnicodeDecodeError)):
        _json.loads(raw)  # surowe bajty nie parsuja sie jako JSON


def test_registry_load_with_wrong_key_raises(tmp_path):
    path = tmp_path / "tokens.bin"
    TokenRegistry(path, key=crypto_lock.generate_key()).issue_token("jacek")
    with pytest.raises(CryptoLockError):
        TokenRegistry(path, key=crypto_lock.generate_key())


def test_registry_load_with_wrong_password_raises(tmp_path):
    path = tmp_path / "tokens.bin"
    TokenRegistry(path, password="wlasciwe-haslo").issue_token("jacek")
    with pytest.raises(CryptoLockError):
        TokenRegistry(path, password="zle-haslo")


def test_registry_loads_existing_file_on_construction(tmp_path):
    path = tmp_path / "tokens.bin"
    key = crypto_lock.generate_key()
    first = TokenRegistry(path, key=key)
    first.issue_token("jacek")

    second = TokenRegistry(path, key=key)
    assert second.get_token("jacek") is not None


def test_registry_insecure_plaintext_opt_out_still_works(tmp_path):
    """Jawny, swiadomy fallback do starego zachowania - dziala, ale
    trzeba go jawnie poprosic."""
    path = tmp_path / "tokens.json"
    registry = TokenRegistry(path, insecure_plaintext=True)
    registry.issue_token("jacek")
    assert b'"jacek"' in path.read_bytes()  # tu CELOWO jawny tekst

    reloaded = TokenRegistry(path, insecure_plaintext=True)
    assert reloaded.get_token("jacek") is not None


def test_sync_full_access_for_all_adds_new_repo_to_existing_tokens(tmp_path, monkeypatch):
    """Bezposredni test scenariusza z proby uzytkownika: 'i pozniejsze
    repo' - nowe repo dopisane do REPOS po wystawieniu tokenu powinno
    trafic do istniejacych tokenow po sync_full_access_for_all()."""
    import timdr_token.token as token_module

    patched_repos = dict(REPOS)
    monkeypatch.setattr(token_module, "REPOS", patched_repos)

    path = tmp_path / "tokens.bin"
    registry = TokenRegistry(path, key=crypto_lock.generate_key())
    token = registry.issue_token("jacek")
    assert "Przyszle-Repo" not in token.permissions

    patched_repos["Przyszle-Repo"] = ["read"]
    registry.sync_full_access_for_all()
    assert registry.get_token("jacek").has_access("Przyszle-Repo", "read")


# ── crypto_lock.py bezposrednio ──────────────────────────────────────

def test_crypto_lock_roundtrip_key_mode():
    key = crypto_lock.generate_key()
    blob = crypto_lock.encrypt_bytes(b"tajna tresc", key=key)
    assert crypto_lock.decrypt_bytes(blob, key=key) == b"tajna tresc"


def test_crypto_lock_roundtrip_password_mode():
    blob = crypto_lock.encrypt_bytes(b"tajna tresc", password="haslo123")
    assert crypto_lock.decrypt_bytes(blob, password="haslo123") == b"tajna tresc"


def test_crypto_lock_tampered_blob_is_rejected():
    key = crypto_lock.generate_key()
    blob = bytearray(crypto_lock.encrypt_bytes(b"nietykalna tresc", key=key))
    blob[-1] ^= 0xFF
    with pytest.raises(CryptoLockError):
        crypto_lock.decrypt_bytes(bytes(blob), key=key)


def test_crypto_lock_rejects_plaintext_looking_data():
    with pytest.raises(CryptoLockError):
        crypto_lock.decrypt_bytes(b'{"jacek": {}}', key=crypto_lock.generate_key())
