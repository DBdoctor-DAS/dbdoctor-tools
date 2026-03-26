"""
config.py - Configuration Management Module

Reads DBDoctor configuration from system environment variables or .env file:
  - DBDOCTOR_URL: API base URL
  - DBDOCTOR_USER: Login username
  - DBDOCTOR_PASSWORD: Login password (encrypted at rest in .env)

Priority: System environment variables > .env file > Interactive input
"""

import os
import sys
import base64
from pathlib import Path

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

# List of required environment variables
_REQUIRED_ENV_VARS = ("DBDOCTOR_URL", "DBDOCTOR_USER", "DBDOCTOR_PASSWORD")

# Storage encryption key (for .env file at-rest encryption only)
_STORAGE_KEY = b"dbdoctor-tools!!dbdoctor-tools!!"  # 32 bytes for AES-256

# Prefix to identify encrypted values
_ENC_PREFIX = "ENC:"


def _encrypt_for_storage(plaintext: str) -> str:
    """Encrypt a value for storage in .env file, return ENC: prefixed string."""
    cipher = AES.new(_STORAGE_KEY, AES.MODE_ECB)
    padded = pad(plaintext.encode("utf-8"), AES.block_size)
    encrypted = cipher.encrypt(padded)
    return _ENC_PREFIX + base64.b64encode(encrypted).decode("utf-8")


def _decrypt_from_storage(value: str) -> str:
    """Decrypt an ENC: prefixed value from .env file. Returns plaintext as-is."""
    if not value.startswith(_ENC_PREFIX):
        return value
    encrypted = base64.b64decode(value[len(_ENC_PREFIX):])
    cipher = AES.new(_STORAGE_KEY, AES.MODE_ECB)
    decrypted = unpad(cipher.decrypt(encrypted), AES.block_size)
    return decrypted.decode("utf-8")


class ConfigError(Exception):
    """Configuration error exception"""
    pass


def is_interactive():
    """Check if running in an interactive terminal environment"""
    return sys.stdin.isatty() and sys.stdout.isatty()


def interactive_init():
    """
    Interactive configuration wizard
    Guides user to input DBDoctor configuration
    """
    print("=" * 60)
    print("Welcome to dbdoctor-tools!")
    print("First-time configuration required.")
    print("=" * 60)
    print()

    # Input DBDoctor URL
    while True:
        url = input("Please enter DBDoctor URL (e.g., http://localhost:8080): ").strip()
        if url:
            # Simple URL format validation
            if not (url.startswith("http://") or url.startswith("https://")):
                print("❌ Invalid URL format. Please start with http:// or https://")
                continue
            break
        print("❌ URL cannot be empty. Please try again.")

    # Input username
    while True:
        user = input("Please enter DBDoctor username: ").strip()
        if user:
            break
        print("❌ Username cannot be empty. Please try again.")

    # Input password (hidden)
    try:
        import getpass
        while True:
            password = getpass.getpass("Please enter DBDoctor password: ").strip()
            if password:
                break
            print("❌ Password cannot be empty. Please try again.")
    except Exception:
        # Fallback to regular input if getpass fails
        while True:
            password = input("Please enter DBDoctor password: ").strip()
            if password:
                break
            print("❌ Password cannot be empty. Please try again.")

    return url, user, password


def generate_env_file(url, user, password):
    """
    Generate .env configuration file with encrypted password.
    
    Args:
        url: DBDoctor URL
        user: Username
        password: Password (plaintext, will be encrypted before storage)
    
    Returns:
        Path: Path to the generated file
    """
    env_path = Path(__file__).parent.parent / '.env'
    
    encrypted_password = _encrypt_for_storage(password)
    
    env_content = f"""# DBDoctor Configuration File
# This file is auto-generated and contains sensitive information.
# DO NOT commit this file to version control.

# DBDoctor API Base URL
DBDOCTOR_URL={url}

# Login Username (also used as UserId)
DBDOCTOR_USER={user}

# Login Password (AES encrypted at rest, decrypted automatically at runtime)
DBDOCTOR_PASSWORD={encrypted_password}
"""
    
    # Write file
    env_path.write_text(env_content, encoding='utf-8')
    
    # Set file permissions (Unix systems only)
    try:
        os.chmod(env_path, 0o600)
    except Exception:
        # Windows or other systems may not support this, ignore error
        pass
    
    return env_path


def _auto_encrypt_env_password():
    """
    Check .env file and auto-encrypt plaintext DBDOCTOR_PASSWORD in place.
    If the password value does not start with ENC: prefix, encrypt it and rewrite the file.
    """
    env_path = Path(__file__).parent.parent / '.env'
    if not env_path.exists():
        return

    try:
        content = env_path.read_text(encoding='utf-8')
    except Exception:
        return

    lines = content.splitlines(keepends=True)
    new_lines = []
    changed = False

    for line in lines:
        stripped = line.strip()
        if stripped.startswith("DBDOCTOR_PASSWORD="):
            value = stripped[len("DBDOCTOR_PASSWORD="):]
            if value and not value.startswith(_ENC_PREFIX):
                encrypted = _encrypt_for_storage(value)
                new_lines.append(f"DBDOCTOR_PASSWORD={encrypted}\n")
                # Also update the environment variable so dotenv picks up the encrypted value
                os.environ["DBDOCTOR_PASSWORD"] = encrypted
                changed = True
                continue
        new_lines.append(line)

    if changed:
        env_path.write_text("".join(new_lines), encoding='utf-8')
        try:
            os.chmod(env_path, 0o600)
        except Exception:
            pass


def try_load_dotenv():
    """Try to load .env file"""
    try:
        from dotenv import load_dotenv
        env_path = Path(__file__).parent.parent / '.env'
        if env_path.exists():
            load_dotenv(dotenv_path=env_path)
            # Auto-encrypt plaintext password if found
            _auto_encrypt_env_password()
            return True
    except ImportError:
        pass
    return False


def check_env_vars():
    """Check if all required environment variables are set"""
    missing = [k for k in _REQUIRED_ENV_VARS if not os.environ.get(k)]
    return len(missing) == 0, missing


class Config:
    """DBDoctor Configuration Management"""

    def __init__(self):
        # First check system environment variables
        env_complete, missing = check_env_vars()
        
        if not env_complete:
            # Try to load .env file
            try_load_dotenv()
            
            # Check again
            env_complete, missing = check_env_vars()
            
            if not env_complete:
                # Environment variables still incomplete, trigger auto-initialization
                if not is_interactive():
                    raise ConfigError(
                        f"Missing required environment variables: {', '.join(missing)}\n\n"
                        f"Currently running in non-interactive environment. Cannot auto-configure.\n"
                        f"Please configure using one of the following methods:\n"
                        f"1. Set system environment variables:\n"
                        f"   DBDOCTOR_URL=http://[host]:[port]\n"
                        f"   DBDOCTOR_USER=[username]\n"
                        f"   DBDOCTOR_PASSWORD=[password]\n"
                        f"2. Run in an interactive terminal for guided configuration\n"
                        f"3. Manually create .env file with DBDOCTOR_URL, DBDOCTOR_USER, DBDOCTOR_PASSWORD"
                    )
                
                # Interactive initialization
                url, user, password = interactive_init()
                
                # Generate .env file
                env_path = generate_env_file(url, user, password)
                
                print()
                print("=" * 60)
                print(f"✅ Configuration saved to: {env_path}")
                print("=" * 60)
                print()
                
                # Reload .env file
                try_load_dotenv()
                
                # Final check
                env_complete, missing = check_env_vars()
                if not env_complete:
                    raise ConfigError(
                        f"Configuration initialization failed. Still missing: {', '.join(missing)}"
                    )

        self.base_url = os.environ["DBDOCTOR_URL"]
        self.username = os.environ["DBDOCTOR_USER"]
        self.password = _decrypt_from_storage(os.environ["DBDOCTOR_PASSWORD"])
        # Username is used as UserId
        self.user_id = self.username
        # Role hardcoded as dev
        self.role = "dev"


# Global configuration singleton
config = Config()
