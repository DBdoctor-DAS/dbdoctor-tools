"""
config.py - Configuration Management Module

Reads DBDoctor configuration from system environment variables or .env file:
  - DBDOCTOR_URL: API base URL
  - DBDOCTOR_USER: Login username
  - DBDOCTOR_PASSWORD: Login password (plaintext)

Priority: System environment variables > .env file > Interactive input
"""

import os
import sys
from pathlib import Path

# List of required environment variables
_REQUIRED_ENV_VARS = ("DBDOCTOR_URL", "DBDOCTOR_USER", "DBDOCTOR_PASSWORD")


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
    Generate .env configuration file
    
    Args:
        url: DBDoctor URL
        user: Username
        password: Password
    
    Returns:
        Path: Path to the generated file
    """
    env_path = Path(__file__).parent.parent / '.env'
    
    env_content = f"""# DBDoctor Configuration File
# This file is auto-generated and contains sensitive information.
# DO NOT commit this file to version control.

# DBDoctor API Base URL
DBDOCTOR_URL={url}

# Login Username (also used as UserId)
DBDOCTOR_USER={user}

# Login Password (stored in plaintext, will be AES encrypted by the program)
DBDOCTOR_PASSWORD={password}
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


def try_load_dotenv():
    """Try to load .env file"""
    try:
        from dotenv import load_dotenv
        env_path = Path(__file__).parent.parent / '.env'
        if env_path.exists():
            load_dotenv(dotenv_path=env_path)
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
                        f"3. Manually create .env file (see .env.example)"
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
        self.password = os.environ["DBDOCTOR_PASSWORD"]
        # Username is used as UserId
        self.user_id = self.username
        # Role hardcoded as dev
        self.role = "dev"


# Global configuration singleton
config = Config()
