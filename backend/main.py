try:
    from app import create_app
except ImportError:  # Supports running as `uvicorn backend.main:app` from repo root.
    from backend.app import create_app

app = create_app()
