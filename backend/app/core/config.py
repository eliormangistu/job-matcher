import importlib
import os
from pathlib import Path

from dotenv import load_dotenv


BASE_DIR = Path(__file__).resolve().parents[2]

load_dotenv(BASE_DIR / ".env")

APP_ENV = os.getenv("APP_ENV", "dev")

ENV_FILE = BASE_DIR / "env" / f".env.{APP_ENV}"
load_dotenv(ENV_FILE, override=True)


try:
    config = importlib.import_module(f"config.{APP_ENV}_config")
except ModuleNotFoundError as exc:
    raise RuntimeError(f"Unknown environment: {APP_ENV}") from exc


globals().update(
    {name: getattr(config, name) for name in dir(config) if not name.startswith("_")}
)
