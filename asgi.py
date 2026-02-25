"""
ASGI adapter for running Flask app with Uvicorn
"""
from a2wsgi import ASGIMiddleware
from app import app

# Wrap Flask WSGI app in ASGI middleware
application = ASGIMiddleware(app)
