"""
config.py - Configuration Management Module

Reads DBDoctor configuration from environment variables:
  - DBDOCTOR_URL: API base URL
  - DBDOCTOR_USER: Login username
  - DBDOCTOR_PASSWORD: Login password

Priority: System / platform-injected environment variables > .env file (legacy fallback)
"""

import os
import base64
from pathlib import Path

from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

# List of required environment variables
_REQUIRED_ENV_VARS = ("DBDOCTOR_URL", "DBDOCTOR_USER", "DBDOCTOR_PASSWORD")

# Storage encryption key (for decrypting legacy ENC: prefixed values in .env)
_STORAGE_KEY = b"dbdoctor-tools!!dbdoctor-tools!!"  # 32 bytes for AES-256

# Prefix to identify encrypted values
_ENC_PREFIX = "ENC:"


def _decrypt_from_storage(value: str) -> str:
    """Decrypt an ENC: prefixed value from legacy .env file. Returns plaintext as-is."""
    if not value.startswith(_ENC_PREFIX):
        return value
    encrypted = base64.b64decode(value[len(_ENC_PREFIX):])
    cipher = AES.new(_STORAGE_KEY, AES.MODE_ECB)
    decrypted = unpad(cipher.decrypt(encrypted), AES.block_size)
    return decrypted.decode("utf-8")


class ConfigError(Exception):
    """Configuration error exception"""
    pass


def _try_load_dotenv():
    """Try to load .env file (legacy fallback)"""
    try:
        from dotenv import load_dotenv
        env_path = Path(__file__).parent.parent / '.env'
        if env_path.exists():
            load_dotenv(dotenv_path=env_path)
            return True
    except ImportError:
        pass
    return False


def _check_env_vars():
    """Check if all required environment variables are set"""
    missing = [k for k in _REQUIRED_ENV_VARS if not os.environ.get(k)]
    return len(missing) == 0, missing


class Config:
    """DBDoctor Configuration Management"""

    def __init__(self):
        # First check system / platform-injected environment variables
        env_complete, missing = _check_env_vars()

        if not env_complete:
            # Fallback: try to load legacy .env file
            _try_load_dotenv()
            env_complete, missing = _check_env_vars()

            if not env_complete:
                raise ConfigError(
                    f"Missing required environment variables: {', '.join(missing)}\n\n"
                    f"Please configure using one of the following methods:\n"
                    f"1. Platform CLI (recommended):\n"
                    f"   clawdbot skills config dbdoctor-tools DBDOCTOR_URL \"http://[host]:[port]\"\n"
                    f"   clawdbot skills config dbdoctor-tools DBDOCTOR_USER \"[username]\"\n"
                    f"   clawdbot skills config dbdoctor-tools DBDOCTOR_PASSWORD \"[password]\"\n"
                    f"2. System environment variables:\n"
                    f"   export DBDOCTOR_URL=http://[host]:[port]\n"
                    f"   export DBDOCTOR_USER=[username]\n"
                    f"   export DBDOCTOR_PASSWORD=[password]"
                )

        self.base_url = os.environ["DBDOCTOR_URL"]
        self.username = os.environ["DBDOCTOR_USER"]
        # Support legacy ENC: prefixed passwords from old .env files
        self.password = _decrypt_from_storage(os.environ["DBDOCTOR_PASSWORD"])
        # Username is used as UserId
        self.user_id = self.username
        # Role hardcoded as dev
        self.role = "dev"


# Global configuration singleton
config = Config()
