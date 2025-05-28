"""
Google authentication service for Calendar API.
Handles Service Account authentication to access Google Calendar API
for creating events with Google Meet links.
"""

import json
import logging
import os
from typing import Optional

from google.auth.transport.requests import Request
from google.oauth2 import service_account
from googleapiclient.discovery import build

logger = logging.getLogger(__name__)


class GoogleAuthService:
    """Handles Google API authentication using Service Account."""
    
    # Required scopes for Google Calendar API with Meet integration
    SCOPES = [
        'https://www.googleapis.com/auth/calendar.events',  # Calendar events management
        'https://www.googleapis.com/auth/calendar'          # Full calendar access
    ]
    
    def __init__(self):
        """Initialize the authentication service."""
        self.credentials = None
        self._service_account_path = None
    
    def _get_service_account_path(self) -> str:
        """Get the path to the service account credentials file."""
        # Try different possible locations
        possible_paths = [
            os.path.expanduser("~/credentials/meet_the_bot/service-account.json"),
            os.path.join(os.path.dirname(__file__), "../../../credentials/service-account.json"),
            os.path.join(os.path.dirname(__file__), "../../service-account.json"),
            "service-account.json"
        ]
        
        for path in possible_paths:
            if os.path.exists(path):
                return path
        
        return possible_paths[0]  # Return default path
    
    def get_credentials(self):
        """Get authenticated credentials for Google APIs."""
        if self.credentials and self.credentials.valid:
            return self.credentials
        
        service_account_path = self._get_service_account_path()
        if not service_account_path:
            logger.error("Service account path not configured")
            return None
        
        if not os.path.exists(service_account_path):
            logger.error(f"Service account file does not exist: {service_account_path}")
            return None
        
        try:
            # Load service account credentials
            self.credentials = service_account.Credentials.from_service_account_file(
                service_account_path,
                scopes=self.SCOPES
            )
            
            # Refresh credentials if needed
            if not self.credentials.valid:
                if self.credentials.expired and self.credentials.refresh_token:
                    self.credentials.refresh(Request())
            
            logger.info("Successfully loaded and validated Google credentials")
            return self.credentials
            
        except Exception as e:
            logger.error(f"Failed to load service account credentials: {e}")
            return None
    
    def test_authentication(self) -> dict:
        """
        Test Google API authentication.
        
        Returns:
            Dict with authentication test results
        """
        result = {
            "authenticated": False,
            "service_account_file_exists": False,
            "credentials_loaded": False,
            "calendar_client_created": False,
            "error": None
        }
        
        try:
            # Check if service account file exists
            service_account_path = self._get_service_account_path()
            result["service_account_file_exists"] = service_account_path and os.path.exists(service_account_path)
            
            if not result["service_account_file_exists"]:
                result["error"] = f"Service account file not found at: {service_account_path}"
                return result
            
            # Try to load credentials
            credentials = self.get_credentials()
            result["credentials_loaded"] = credentials is not None
            
            if not result["credentials_loaded"]:
                result["error"] = "Failed to load service account credentials"
                return result
            
            # Try to create Calendar API client
            calendar_service = build('calendar', 'v3', credentials=credentials)
            result["calendar_client_created"] = calendar_service is not None
            
            if not result["calendar_client_created"]:
                result["error"] = "Failed to create Google Calendar API client"
                return result
            
            # If we got here, authentication is successful
            result["authenticated"] = True
            logger.info("Google API authentication test successful")
            
        except Exception as e:
            error_msg = f"Authentication test failed: {str(e)}"
            logger.error(error_msg)
            result["error"] = error_msg
        
        return result


# Global instance
auth_service = GoogleAuthService()


def get_google_auth_service() -> GoogleAuthService:
    """Get the global Google authentication service instance."""
    return auth_service 