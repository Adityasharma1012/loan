"""Root Application Entrypoint for Cloud Hosting (Render, Heroku, Docker).
Delegates to the loan-xai FastAPI application.
"""

import sys
from pathlib import Path

# Add backend directory to sys.path so app packages import cleanly
ROOT_DIR = Path(__file__).resolve().parent
BACKEND_DIR = ROOT_DIR / "loan-xai" / "backend"

if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

# Import the configured FastAPI app
from app.main import app  # noqa: E402
