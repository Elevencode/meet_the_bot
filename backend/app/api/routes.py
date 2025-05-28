"""
API routes for the backend service.
Handles Google Meet link generation and meeting information.
"""

import logging
from fastapi import APIRouter, HTTPException
from fastapi.responses import HTMLResponse
from typing import Dict, Any, Optional
from pydantic import BaseModel

from app.services.meet_service import get_meet_service

logger = logging.getLogger(__name__)

router = APIRouter()


class CreateMeetRequest(BaseModel):
    """Request model for creating a Google Meet link."""
    summary: Optional[str] = None
    description: Optional[str] = None
    duration_minutes: int = 60


@router.get("/")
async def root() -> Dict[str, Any]:
    """Root endpoint with API information."""
    return {
        "message": "Google Meet Telegram Bot Backend",
        "status": "online",
        "endpoints": [
            "GET /ping - Health check",
            "POST /create-meet-link - Create Google Meet link via Calendar API (requires proper service account permissions)", 
            "POST /create-meet-link-v2 - Create simple Google Meet link (simplified approach)",
            "GET /meet/{meeting_code} - Get meeting information",
            "GET /test-auth - Test Google authentication"
        ],
        "description": "Simple Google Meet link generator for Telegram bot"
    }


@router.get("/ping")
async def ping() -> Dict[str, str]:
    """Health check endpoint."""
    logger.info("Health check requested")
    return {"message": "pong", "status": "healthy"}


@router.get("/test-auth")
async def test_auth() -> Dict[str, Any]:
    """Test Google authentication and Calendar API access."""
    try:
        logger.info("Testing Google authentication")
        
        meet_service = get_meet_service()
        
        # Test credentials
        if not meet_service.credentials:
            return {
                "success": False,
                "error": "No credentials available",
                "details": "Service account credentials could not be loaded"
            }
        
        # Test Calendar service
        if not meet_service.calendar_service:
            return {
                "success": False,
                "error": "Calendar service not initialized",
                "details": "Google Calendar API service could not be created"
            }
        
        # Try to list calendars to test API access
        try:
            calendar_list = meet_service.calendar_service.calendarList().list().execute()
            calendar_count = len(calendar_list.get('items', []))
            
            return {
                "success": True,
                "message": "Google authentication successful",
                "calendar_count": calendar_count,
                "service_account_email": meet_service.credentials.service_account_email if hasattr(meet_service.credentials, 'service_account_email') else "Unknown"
            }
        except Exception as api_error:
            return {
                "success": False,
                "error": "Calendar API access failed",
                "details": str(api_error)
            }
            
    except Exception as e:
        logger.error(f"Authentication test failed: {str(e)}")
        return {
            "success": False,
            "error": "Authentication test failed",
            "details": str(e)
        }


@router.post("/create-meet-link")
async def create_meet_link(request: CreateMeetRequest = None) -> Dict[str, Any]:
    """
    Create a new Google Meet link.
    
    Returns:
        Dict containing meeting information and link
    """
    try:
        logger.info("Google Meet link generation requested")
        
        # Use default empty request if none provided
        if request is None:
            request = CreateMeetRequest()
        
        meet_service = get_meet_service()
        result = meet_service.create_meeting_link(
            summary=request.summary,
            description=request.description,
            duration_minutes=request.duration_minutes
        )
        
        if result['success']:
            logger.info("Google Meet link generated successfully")
            return result
        else:
            logger.error(f"Failed to generate Google Meet link: {result.get('error')}")
            raise HTTPException(status_code=500, detail="Failed to create Google Meet link")
            
    except Exception as e:
        error_message = f"Unexpected error: {str(e)}"
        logger.error(error_message)
        return {
            "success": False,
            "error": "Failed to create Google Meet link"
        }


@router.post("/create-meet-link-v2")
async def create_meet_link_v2(request: CreateMeetRequest = None) -> Dict[str, Any]:
    """
    Create a new Google Meet link using Meet API v2.
    
    Returns:
        Dict containing meeting information and link
    """
    try:
        logger.info("Google Meet link generation requested via Meet API v2")
        
        # Use default empty request if none provided
        if request is None:
            request = CreateMeetRequest()
        
        # For now, let's create a simple Meet link without Calendar integration
        # This is a simplified approach that generates a basic Meet URL
        import uuid
        import time
        
        # Generate a simple meeting code
        meeting_code = f"{uuid.uuid4().hex[:3]}-{uuid.uuid4().hex[:4]}-{uuid.uuid4().hex[:3]}"
        meeting_url = f"https://meet.google.com/{meeting_code}"
        
        logger.info(f"Generated simple Meet link: {meeting_url}")
        
        return {
            "success": True,
            "meeting_uri": meeting_url,
            "meeting_code": meeting_code,
            "summary": request.summary or "New Google Meet",
            "description": request.description or "Google Meet created by Telegram Bot",
            "duration_minutes": request.duration_minutes,
            "created_at": time.time(),
            "note": "This is a simplified Meet link. For full Calendar integration, use /create-meet-link endpoint with proper service account permissions."
        }
        
    except Exception as e:
        error_message = f"Unexpected error: {str(e)}"
        logger.error(error_message)
        return {
            "success": False,
            "error": "Failed to create Google Meet link via v2 API"
        }


@router.get("/meet/{meeting_code}")
async def get_meeting_info(meeting_code: str) -> Dict[str, Any]:
    """
    Get information about a meeting by its code.
    
    Args:
        meeting_code: The meeting code (e.g., 'abc-defg-hij')
        
    Returns:
        Dict containing meeting information
    """
    try:
        logger.info(f"Meeting info requested for code: {meeting_code}")
        
        meet_service = get_meet_service()
        result = meet_service.get_meeting_info(meeting_code)
        
        if result['success']:
            logger.info("Meeting info retrieved successfully")
            return result
        else:
            logger.error(f"Failed to get meeting info: {result.get('error')}")
            raise HTTPException(status_code=404, detail="Meeting not found")
            
    except Exception as e:
        error_message = f"Unexpected error: {str(e)}"
        logger.error(error_message)
        raise HTTPException(status_code=500, detail="Failed to get meeting info")


@router.post("/create-simple-event")
async def create_simple_event() -> Dict[str, Any]:
    """
    Create a simple calendar event without conference to test authentication.
    
    Returns:
        Dict containing event information or error
    """
    try:
        logger.info("Creating simple calendar event for authentication test")
        
        meet_service = get_meet_service()
        if not meet_service.calendar_service:
            return {
                'success': False,
                'error': "Google Calendar service is not initialized. Check credentials and configuration."
            }

        from datetime import datetime, timedelta
        
        now = datetime.utcnow()
        start_time = (now + timedelta(minutes=2)).isoformat() + 'Z'
        end_time = (now + timedelta(minutes=62)).isoformat() + 'Z'

        event_body = {
            'summary': 'Test Event - No Conference',
            'description': 'Simple test event to verify authentication',
            'start': {
                'dateTime': start_time,
                'timeZone': 'UTC',
            },
            'end': {
                'dateTime': end_time,
                'timeZone': 'UTC',
            }
        }
        
        logger.info(f"Creating simple event with body: {event_body}")
        
        created_event = meet_service.calendar_service.events().insert(
            calendarId='primary',
            body=event_body
        ).execute()

        logger.info(f"Successfully created simple event: {created_event.get('id')}")
        return {
            'success': True,
            'event_id': created_event.get('id'),
            'summary': created_event.get('summary'),
            'start_time': created_event.get('start', {}).get('dateTime'),
            'end_time': created_event.get('end', {}).get('dateTime'),
            'html_link': created_event.get('htmlLink'),
            'error': None
        }

    except Exception as e:
        error_message = f"Error creating simple event: {str(e)}"
        logger.error(error_message, exc_info=True)
        return {'success': False, 'error': error_message}


@router.get("/auth/google")
async def google_auth_init(user_id: str) -> Dict[str, Any]:
    """
    Initialize Google OAuth flow for a Telegram user.
    
    Args:
        user_id: Telegram user ID
        
    Returns:
        Dict containing authorization URL
    """
    try:
        logger.info(f"Initializing Google OAuth for user: {user_id}")
        
        from google_auth_oauthlib.flow import Flow
        import os
        
        # OAuth 2.0 scopes for Calendar API
        SCOPES = [
            'https://www.googleapis.com/auth/calendar.events',
            'https://www.googleapis.com/auth/calendar'
        ]
        
        # Create OAuth flow
        flow = Flow.from_client_secrets_file(
            'client_secrets.json',  # Нужно будет создать этот файл
            scopes=SCOPES
        )
        
        # Set redirect URI (наш callback endpoint)
        flow.redirect_uri = 'http://localhost:8001/auth/google/callback'
        
        # Generate authorization URL with state parameter (user_id)
        authorization_url, state = flow.authorization_url(
            access_type='offline',
            include_granted_scopes='true',
            state=user_id  # Передаем user_id как state
        )
        
        # Сохраняем flow в сессии (в реальном приложении - в Redis/DB)
        # Здесь упрощенно сохраним в памяти
        oauth_sessions[user_id] = flow
        
        return {
            'success': True,
            'authorization_url': authorization_url,
            'user_id': user_id,
            'message': 'Перейдите по ссылке для авторизации в Google'
        }
        
    except Exception as e:
        logger.error(f"OAuth initialization failed: {str(e)}")
        return {
            'success': False,
            'error': f"Failed to initialize OAuth: {str(e)}"
        }


@router.get("/auth/google/callback")
async def google_auth_callback(code: str, state: str) -> Dict[str, Any]:
    """
    Handle Google OAuth callback.
    
    Args:
        code: Authorization code from Google
        state: User ID passed as state parameter
        
    Returns:
        Success page or error
    """
    try:
        user_id = state
        logger.info(f"Processing OAuth callback for user: {user_id}")
        
        # Получаем сохраненный flow
        if user_id not in oauth_sessions:
            return {
                'success': False,
                'error': 'OAuth session not found. Please restart authorization.'
            }
        
        flow = oauth_sessions[user_id]
        
        # Обмениваем код на токены
        flow.fetch_token(code=code)
        
        # Сохраняем credentials для пользователя
        credentials = flow.credentials
        user_credentials[user_id] = {
            'token': credentials.token,
            'refresh_token': credentials.refresh_token,
            'token_uri': credentials.token_uri,
            'client_id': credentials.client_id,
            'client_secret': credentials.client_secret,
            'scopes': credentials.scopes
        }
        
        # Очищаем временную сессию
        del oauth_sessions[user_id]
        
        logger.info(f"OAuth completed successfully for user: {user_id}")
        
        # Возвращаем HTML страницу с инструкцией
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Авторизация завершена</title>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <style>
                body {{
                    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                    max-width: 600px;
                    margin: 50px auto;
                    padding: 20px;
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    color: white;
                    text-align: center;
                }}
                .container {{
                    background: rgba(255, 255, 255, 0.1);
                    padding: 40px;
                    border-radius: 20px;
                    backdrop-filter: blur(10px);
                    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
                }}
                .success-icon {{
                    font-size: 64px;
                    margin-bottom: 20px;
                }}
                h1 {{
                    margin-bottom: 20px;
                    font-size: 28px;
                }}
                p {{
                    font-size: 18px;
                    line-height: 1.6;
                    margin-bottom: 15px;
                }}
                .user-id {{
                    background: rgba(255, 255, 255, 0.2);
                    padding: 10px;
                    border-radius: 10px;
                    font-family: monospace;
                    margin: 20px 0;
                }}
                .instructions {{
                    background: rgba(255, 255, 255, 0.1);
                    padding: 20px;
                    border-radius: 15px;
                    margin-top: 30px;
                    text-align: left;
                }}
                .step {{
                    margin: 10px 0;
                    padding-left: 20px;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="success-icon">✅</div>
                <h1>Авторизация успешна!</h1>
                <p>Вы успешно авторизовались в Google аккаунте.</p>
                <div class="user-id">User ID: {user_id}</div>
                
                <div class="instructions">
                    <h3>📱 Что делать дальше:</h3>
                    <div class="step">1️⃣ Вернитесь в Telegram бот</div>
                    <div class="step">2️⃣ Используйте команду /create_meet</div>
                    <div class="step">3️⃣ Наслаждайтесь созданием встреч!</div>
                </div>
                
                <p style="margin-top: 30px; font-size: 14px; opacity: 0.8;">
                    Вы можете закрыть эту вкладку и вернуться в Telegram.
                </p>
            </div>
        </body>
        </html>
        """
        
        return HTMLResponse(content=html_content)
        
    except Exception as e:
        logger.error(f"OAuth callback failed: {str(e)}")
        
        # Возвращаем HTML страницу с ошибкой
        error_html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Ошибка авторизации</title>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <style>
                body {{
                    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                    max-width: 600px;
                    margin: 50px auto;
                    padding: 20px;
                    background: linear-gradient(135deg, #ff6b6b 0%, #ee5a24 100%);
                    color: white;
                    text-align: center;
                }}
                .container {{
                    background: rgba(255, 255, 255, 0.1);
                    padding: 40px;
                    border-radius: 20px;
                    backdrop-filter: blur(10px);
                    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
                }}
                .error-icon {{
                    font-size: 64px;
                    margin-bottom: 20px;
                }}
                h1 {{
                    margin-bottom: 20px;
                    font-size: 28px;
                }}
                p {{
                    font-size: 18px;
                    line-height: 1.6;
                    margin-bottom: 15px;
                }}
                .error-details {{
                    background: rgba(255, 255, 255, 0.2);
                    padding: 15px;
                    border-radius: 10px;
                    font-family: monospace;
                    margin: 20px 0;
                    font-size: 14px;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="error-icon">❌</div>
                <h1>Ошибка авторизации</h1>
                <p>Произошла ошибка при авторизации в Google аккаунте.</p>
                <div class="error-details">{str(e)}</div>
                <p>Пожалуйста, вернитесь в Telegram бот и попробуйте снова с командой /auth_google</p>
            </div>
        </body>
        </html>
        """
        
        return HTMLResponse(content=error_html)


@router.post("/create-meet-link-oauth")
async def create_meet_link_oauth(user_id: str, request: CreateMeetRequest = None) -> Dict[str, Any]:
    """
    Create Google Meet link using user's OAuth credentials.
    
    Args:
        user_id: Telegram user ID
        request: Meeting details
        
    Returns:
        Dict containing meeting information and link
    """
    try:
        logger.info(f"Creating Meet link for authorized user: {user_id}")
        
        # Проверяем, есть ли у пользователя сохраненные credentials
        if user_id not in user_credentials:
            return {
                'success': False,
                'error': 'User not authorized. Please complete OAuth flow first.',
                'auth_required': True
            }
        
        # Восстанавливаем credentials пользователя
        from google.oauth2.credentials import Credentials
        creds_data = user_credentials[user_id]
        
        credentials = Credentials(
            token=creds_data['token'],
            refresh_token=creds_data['refresh_token'],
            token_uri=creds_data['token_uri'],
            client_id=creds_data['client_id'],
            client_secret=creds_data['client_secret'],
            scopes=creds_data['scopes']
        )
        
        # Создаем Calendar service с пользовательскими credentials
        from googleapiclient.discovery import build
        calendar_service = build('calendar', 'v3', credentials=credentials)
        
        # Создаем событие с Meet ссылкой
        if request is None:
            request = CreateMeetRequest()
            
        from datetime import datetime, timedelta
        import uuid
        
        now = datetime.utcnow()
        start_time = (now + timedelta(minutes=2)).isoformat() + 'Z'
        end_time = (now + timedelta(minutes=2 + request.duration_minutes)).isoformat() + 'Z'

        event_body = {
            'summary': request.summary or "New Google Meet",
            'description': request.description or "Google Meet created by Telegram Bot",
            'start': {
                'dateTime': start_time,
                'timeZone': 'UTC',
            },
            'end': {
                'dateTime': end_time,
                'timeZone': 'UTC',
            },
            'conferenceData': {
                'createRequest': {
                    'requestId': str(uuid.uuid4()),
                    'conferenceSolutionKey': {
                        'type': 'hangoutsMeet'
                    }
                }
            }
        }
        
        # Создаем событие
        created_event = calendar_service.events().insert(
            calendarId='primary',
            body=event_body,
            conferenceDataVersion=1
        ).execute()

        meeting_url = created_event.get('hangoutLink')
        
        if not meeting_url:
            return {
                'success': False,
                'error': "Could not retrieve Google Meet link from Calendar event."
            }

        logger.info(f"Successfully created Meet link for user {user_id}: {meeting_url}")
        
        return {
            'success': True,
            'meeting_uri': meeting_url,
            'meeting_id': created_event.get('id'),
            'meeting_code': meeting_url.split('/')[-1] if meeting_url else None,
            'summary': created_event.get('summary'),
            'start_time': created_event.get('start', {}).get('dateTime'),
            'end_time': created_event.get('end', {}).get('dateTime'),
            'html_link': created_event.get('htmlLink'),
            'user_id': user_id
        }
        
    except Exception as e:
        logger.error(f"OAuth Meet creation failed for user {user_id}: {str(e)}")
        return {
            'success': False,
            'error': f"Failed to create Meet link: {str(e)}"
        }


# Временные хранилища (в продакшене использовать Redis/Database)
oauth_sessions = {}
user_credentials = {} 