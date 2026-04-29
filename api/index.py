import os
import sys


# Vercel runs this file as the Serverless Function entrypoint.
# Ensure imports work regardless of working directory.
REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BACKEND_DIR = os.path.join(REPO_ROOT, "backend")

# Make `backend/` importable so that `app.*` resolves to `backend/app/*`.
if BACKEND_DIR not in sys.path:
    sys.path.insert(0, BACKEND_DIR)

from fastapi import FastAPI
from app.main import app as backend_app


# Expose an ASGI app for Vercel.
# In production we want endpoints under `/api/*`.
app = FastAPI()
app.mount("/api", backend_app)
