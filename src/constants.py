from pathlib import Path
from typing import Final

BASE_DIR: Final[Path] = Path(__file__).resolve().parent.parent

LOG_DIR: Final[Path] = BASE_DIR / "logs"
LOG_FILE: Final[Path] = LOG_DIR / "bim_project_app_logging.log"
DATE_FORMAT: Final[str] = "%Y-%m-%d"
LOG_FORMAT: Final[str] = '"%(asctime)s - [%(levelname)s] - %(message)s"'

ENV_PATH: Final[Path] = BASE_DIR / r"infra/.env"

STATIC_PATH: Final[Path] = BASE_DIR / "static"

DESCRITPION_FAST_API_APP: Final[str] = """Описание проекта."""
