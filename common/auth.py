"""
auth.py - Authentication and Token management module

Responsibilities:
  - AES encrypt password (ECB/PKCS7 compatible with frontend CryptoJS)
  - Call login API to get authToken
  - Token file cache (.token_cache) and auto refresh
"""

import os
import base64

import requests
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad

from common.config import config

# AES key (same as frontend)
AES_KEY = "loo2vrx79g87luhvj06lodb0c3lp3gqw"

# Token cache file path (in project directory)
_TOKEN_CACHE_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), ".token_cache")


class AuthError(Exception):
    """Authentication error exception"""
    pass


def encrypt_password(plain_password: str, disabled: bool = False) -> str:
    """
    Encrypt password using AES-ECB, return Base64 encoded string.
    Compatible with frontend CryptoJS.AES.encrypt (ECB mode, PKCS7 padding).
    
    Args:
        plain_password: Plaintext password
        disabled: Whether to disable encryption (return plaintext directly)
    """
    if disabled:
        return plain_password
    
    key = AES_KEY.encode("utf-8")
    cipher = AES.new(key, AES.MODE_ECB)
    padded_data = pad(plain_password.encode("utf-8"), AES.block_size)
    encrypted = cipher.encrypt(padded_data)
    return base64.b64encode(encrypted).decode("utf-8")


def _login() -> str:
    """
    Call login API to get authToken.

    POST {base_url}/nephele/login
    Return authToken string, raise AuthError on failure.
    """
    url = f"{config.base_url}/nephele/login"
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json, text/plain, */*",
        
    }
    payload = {
        "userName": config.username,
        "password": encrypt_password(config.password),
    }

    try:
        resp = requests.post(url, json=payload, headers=headers, verify=False, timeout=30)
        resp.raise_for_status()
    except requests.RequestException as e:
        raise AuthError(f"Login request failed: {e}")

    data = resp.json()
    if not data.get("success"):
        raise AuthError(f"Login failed: {data}")

    token = data.get("data", {}).get("authToken")
    if not token:
        raise AuthError(f"authToken not found in login response: {data}")

    return token


def _save_token(token: str) -> None:
    """Write token to cache file"""
    with open(_TOKEN_CACHE_FILE, "w", encoding="utf-8") as f:
        f.write(token)


def _load_token() -> str | None:
    """Read token from cache file, return None if not exists"""
    if not os.path.exists(_TOKEN_CACHE_FILE):
        return None
    try:
        with open(_TOKEN_CACHE_FILE, "r", encoding="utf-8") as f:
            token = f.read().strip()
            return token if token else None
    except Exception:
        return None


def _clear_token() -> None:
    """Clear cached token file"""
    if os.path.exists(_TOKEN_CACHE_FILE):
        os.remove(_TOKEN_CACHE_FILE)


def get_token() -> str:
    """
    Get current valid authToken.
    Read from cache file first, auto login and cache if not exists.
    """
    token = _load_token()
    if token:
        return token

    token = _login()
    _save_token(token)
    return token


def refresh_token() -> str:
    """
    Force refresh token: clear cache → re-login → cache new token.
    """
    _clear_token()
    token = _login()
    _save_token(token)
    return token
