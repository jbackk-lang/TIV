"""
crypto_lock.py — szyfrowanie pliku tokens.json w spoczynku (at rest),
żeby nie leżał jawnym tekstem na dysku. Ten sam realny wzorzec co w
audycie/naprawie repo Helix-Lock (patrz Helix Pro): AES-256-GCM z
audytowanej biblioteki `cryptography`, tryb pliku-klucza LUB hasła
(scrypt + losowa sól). Kod jest tutaj zaszyty bezpośrednio (nie
importowany z Helix-Lock) - to osobne repozytorium, do którego nie mam
dostępu push, więc nie da się z niego bezpiecznie importować jako
zależności; podejście jest jednak celowo identyczne.

CZYM TO JEST: ochrona POUFNOŚCI I INTEGRALNOŚCI pliku `tokens.json` na
dysku - bez właściwego klucza/hasła nie da się ani odczytać zawartości,
ani zmodyfikować pliku tak, żeby modyfikacja przeszła niezauważona
(AES-GCM ma wbudowaną autentykację - każda zmiana bajtu unieważnia
odszyfrowanie).

CZYM TO NIE JEST: to nadal NIE jest system uprawnień GitHub (patrz
zastrzeżenie w token.py/repos.py) i nie chroni przed kimś, kto zna
Twoje hasło/ma Twój plik klucza - zarządzanie kluczem/hasłem
(przechowywanie go bezpiecznie, osobno od tokens.json) to Twoja
odpowiedzialność, nie coś, co ten moduł może wymusić.
"""
from __future__ import annotations

import os
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt
from cryptography.exceptions import InvalidTag

MAGIC = b"TTOK"
VERSION = 1
MODE_KEY = b"\x01"
MODE_PASSWORD = b"\x02"

SALT_SIZE = 16
NONCE_SIZE = 12
KEY_SIZE = 32

SCRYPT_N = 2 ** 14
SCRYPT_R = 8
SCRYPT_P = 1


class CryptoLockError(Exception):
    """Zly klucz/haslo, uszkodzony/zmanipulowany plik, albo plik w
    starym (sprzed szyfrowania) formacie jawnego JSON-a."""


def generate_key() -> bytes:
    """32 losowe bajty na tryb pliku-klucza. Przechowuj ten plik
    OSOBNO od tokens.json (inny folder/nosnik) - trzymanie obu razem
    niweczy sens szyfrowania."""
    return AESGCM.generate_key(bit_length=256)


def derive_key_from_password(password: str, salt: bytes) -> bytes:
    kdf = Scrypt(salt=salt, length=KEY_SIZE, n=SCRYPT_N, r=SCRYPT_R, p=SCRYPT_P)
    return kdf.derive(password.encode("utf-8"))


def encrypt_bytes(plaintext: bytes, *, key: bytes | None = None, password: str | None = None) -> bytes:
    """Zwraca pelny blob z naglowkiem (MAGIC+wersja+tryb+[sol]+nonce+ciphertext),
    gotowy do zapisania na dysk. Podaj dokladnie jedno z key/password."""
    if (key is None) == (password is None):
        raise CryptoLockError("podaj dokladnie jedno z: key, password")

    nonce = os.urandom(NONCE_SIZE)
    if key is not None:
        if len(key) != KEY_SIZE:
            raise CryptoLockError(f"klucz musi miec {KEY_SIZE} bajtow, dostano {len(key)}")
        ct = AESGCM(key).encrypt(nonce, plaintext, None)
        return MAGIC + bytes([VERSION]) + MODE_KEY + nonce + ct

    salt = os.urandom(SALT_SIZE)
    derived = derive_key_from_password(password, salt)
    ct = AESGCM(derived).encrypt(nonce, plaintext, None)
    return MAGIC + bytes([VERSION]) + MODE_PASSWORD + salt + nonce + ct


def decrypt_bytes(blob: bytes, *, key: bytes | None = None, password: str | None = None) -> bytes:
    if (key is None) == (password is None):
        raise CryptoLockError("podaj dokladnie jedno z: key, password")

    if blob[:4] != MAGIC:
        raise CryptoLockError(
            "nieznany format pliku (brak naglowka szyfrowania) - jesli to stary, "
            "jawny tokens.json sprzed wlaczenia szyfrowania, usun go recznie i "
            "wystaw tokeny ponownie przez TokenRegistry z kluczem/haslem"
        )
    version = blob[4]
    if version != VERSION:
        raise CryptoLockError(f"nieobslugiwana wersja formatu: {version}")
    mode = blob[5:6]

    try:
        if mode == MODE_KEY:
            if key is None:
                raise CryptoLockError("ten plik jest w trybie klucza - podaj key, nie password")
            if len(key) != KEY_SIZE:
                raise CryptoLockError(f"klucz musi miec {KEY_SIZE} bajtow, dostano {len(key)}")
            nonce, ct = blob[6:6 + NONCE_SIZE], blob[6 + NONCE_SIZE:]
            return AESGCM(key).decrypt(nonce, ct, None)
        elif mode == MODE_PASSWORD:
            if password is None:
                raise CryptoLockError("ten plik jest w trybie hasla - podaj password, nie key")
            salt = blob[6:6 + SALT_SIZE]
            nonce_start = 6 + SALT_SIZE
            nonce, ct = blob[nonce_start:nonce_start + NONCE_SIZE], blob[nonce_start + NONCE_SIZE:]
            derived = derive_key_from_password(password, salt)
            return AESGCM(derived).decrypt(nonce, ct, None)
        else:
            raise CryptoLockError(f"nieznany tryb w naglowku: {mode!r}")
    except InvalidTag as exc:
        raise CryptoLockError(
            "nie udalo sie odszyfrowac - zly klucz/haslo albo plik zostal zmanipulowany/uszkodzony"
        ) from exc
