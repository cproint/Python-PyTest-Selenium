import os
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()

def _bool_env(name: str, default: str = "false") -> bool:
    return os.getenv(name, default).strip().lower() in ("1", "true", "yes", "y")

@dataclass(frozen=True)
class Settings:
    base_url: str = os.getenv("SAUCE_BASE_URL", "https://www.saucedemo.com")
    username: str = os.getenv("SAUCE_USERNAME", "standard_user")
    password: str = os.getenv("SAUCE_PASSWORD", "secret_sauce")
    browser: str = os.getenv("BROWSER", "chrome").lower()
    headless: bool = _bool_env("HEADLESS", "false")

settings = Settings()
