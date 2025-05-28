"""
Google API authentication service.
Handles service account authentication for Google Meet API.
"""

import os
from typing import Optional
from google.auth.transport.requests import Request
from google.oauth2 import service_account
from google.apps import meet_v2

from app.config import get_settings
from app.core.logger import get_logger

logger = get_logger(__name__)

# Google Meet API scopes
SCOPES = [
    'https://www.googleapis.com/auth/meetings.space.created',
]


class GoogleAuthService:
    """Service for Google API authentication."""
    
    def __init__(self):
        self.settings = get_settings()
        self._credentials = None
        self._meet_client = None
    
    def _load_credentials(self) -> Optional[service_account.Credentials]:
        """Load service account credentials from JSON file."""
        if not self.settings.google_service_account_path:
            logger.error("Google service account path not configured")
            return None
        
        if not os.path.exists(self.settings.google_service_account_path):
            logger.error(f"Service account file not found: {self.settings.google_service_account_path}")
            return None
        
        try:
            credentials = service_account.Credentials.from_service_account_file(
                self.settings.google_service_account_path,
                scopes=SCOPES
            )
            logger.info("Successfully loaded service account credentials")
            return credentials
        except Exception as e:
            logger.error(f"Failed to load service account credentials: {e}")
            return None
    
    def get_credentials(self) -> Optional[service_account.Credentials]:
        """Get authenticated credentials for Google API."""
        if self._credentials is None:
            self._credentials = self._load_credentials()
        
        if self._credentials and self._credentials.expired:
            try:
                self._credentials.refresh(Request())
                logger.info("Refreshed expired credentials")
            except Exception as e:
                logger.error(f"Failed to refresh credentials: {e}")
                return None
        
        return self._credentials
    
    def get_meet_client(self) -> Optional[meet_v2.SpacesServiceClient]:
        """Get authenticated Google Meet API client."""
        if self._meet_client is None:
            credentials = self.get_credentials()
            if not credentials:
                return None
            
            try:
                self._meet_client = meet_v2.SpacesServiceClient(credentials=credentials)
                logger.info("Successfully created Google Meet API client")
            except Exception as e:
                logger.error(f"Failed to create Google Meet API client: {e}")
                return None
        
        return self._meet_client
    
    def test_authentication(self) -> dict:
        """Test Google API authentication."""
        result = {
            "authenticated": False,
            "service_account_file_exists": False,
            "credentials_loaded": False,
            "meet_client_created": False,
            "error": None
        }
        
        try:
            # Check if service account file exists
            if self.settings.google_service_account_path:
                result["service_account_file_exists"] = os.path.exists(
                    self.settings.google_service_account_path
                )
            
            # Try to load credentials
            credentials = self.get_credentials()
            if credentials:
                result["credentials_loaded"] = True
                
                # Try to create Meet client
                meet_client = self.get_meet_client()
                if meet_client:
                    result["meet_client_created"] = True
                    result["authenticated"] = True
            
        except Exception as e:
            result["error"] = str(e)
            logger.error(f"Authentication test failed: {e}")
        
        return result


# Global instance
google_auth_service = GoogleAuthService()


def get_google_auth_service() -> GoogleAuthService:
    """Get the global Google authentication service instance."""
    return google_auth_service 