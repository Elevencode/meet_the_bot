"""
Main entry point for the backend service.
Run this file to start the FastAPI server.
"""

import uvicorn

from app.main import app
from app.config import get_settings
from app.core.logger import setup_logging, get_logger

# Set up logging
setup_logging()
logger = get_logger(__name__)


def main():
    """Main function to run the FastAPI server."""
    settings = get_settings()
    
    # logger.info(f"Loaded settings: google_service_account_path='{settings.google_service_account_path}'") # Log it too

    logger.info(f"Attempting to start server on {settings.host}:{settings.port} from main.py settings")
    
    uvicorn.run(
        app,
        host=settings.host,
        port=settings.port,
        reload=settings.debug,
        log_level=settings.log_level.lower()
    )


if __name__ == "__main__":
    main() 