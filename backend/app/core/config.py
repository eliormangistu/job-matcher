import os
from pathlib import Path
from dotenv import load_dotenv


BASE_DIR = Path(__file__).resolve().parents[2]

load_dotenv(BASE_DIR / ".env")

APP_ENV = os.getenv("APP_ENV", "dev")

ENV_FILE = BASE_DIR / "env" / f".env.{APP_ENV}"

load_dotenv(ENV_FILE, override=True)

if APP_ENV == "dev":
    from config.dev_config import *

elif APP_ENV == "test":
    from config.test_config import *

elif APP_ENV == "prod":
    from config.prod_config import *

else:
    raise RuntimeError(f"Unknown environment: {APP_ENV}")
