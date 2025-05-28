# Google Meet Telegram Bot - Setup Instructions

This guide helps you set up the Google Meet Telegram Bot backend service.

## Prerequisites

- Python 3.8 or higher
- Google Cloud Platform account
- Telegram Bot Token

## Google Cloud Setup

### 1. Create Google Cloud Project

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing one
3. Note your **Project ID**

### 2. Enable Required APIs

**Enable Google Calendar API:**
1. Go to [Google Calendar API](https://console.developers.google.com/apis/api/calendar-json.googleapis.com/overview)
2. Select your project
3. Click **"Enable"**
4. Wait a few minutes for activation

### 3. Create Service Account

1. Go to **IAM & Admin** → **Service Accounts**
2. Click **"Create Service Account"**
3. Fill in details:
   - **Name**: `meet-the-bot-service`
   - **Description**: `Service account for Google Meet bot`
4. Click **"Create and Continue"**

### 4. Grant Permissions

**Add these roles to your Service Account:**
1. **Basic roles** → **Editor** (or more specific roles if preferred)
2. **Google Calendar API** → **Calendar API User**

### 5. Generate Service Account Key

1. Click on your service account
2. Go to **"Keys"** tab
3. Click **"Add Key"** → **"Create new key"**
4. Choose **JSON** format
5. Download the JSON file

### 6. Secure Service Account File

```bash
# Create secure directory
mkdir -p ~/credentials/meet_the_bot

# Move downloaded file (replace 'downloaded-file.json' with actual filename)
mv ~/Downloads/your-service-account-file.json ~/credentials/meet_the_bot/service-account.json

# Set secure permissions
chmod 600 ~/credentials/meet_the_bot/service-account.json
```

## Backend Setup

### 1. Clone Repository

```bash
git clone https://github.com/Elevencode/meet_the_bot.git
cd meet_the_bot
```

### 2. Create Virtual Environment

```bash
python -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment

Create `.env` file in project root:

```bash
# Backend Configuration
HOST=0.0.0.0
PORT=8000
DEBUG=true
LOG_LEVEL=INFO

# Google API Configuration
GOOGLE_SERVICE_ACCOUNT_PATH=~/credentials/meet_the_bot/service-account.json

# Telegram Bot Configuration
TELEGRAM_BOT_TOKEN=your_telegram_bot_token_here
```

### 5. Test Setup

```bash
cd backend
python main.py
```

In another terminal, test authentication:

```bash
curl http://localhost:8000/auth/test
```

Expected response:
```json
{
  "authenticated": true,
  "service_account_file_exists": true,
  "credentials_loaded": true,
  "calendar_client_created": true,
  "error": null
}
```

Test meeting creation:

```bash
curl -X POST http://localhost:8000/create-meet-link
```

Expected response:
```json
{
  "success": true,
  "meeting_uri": "https://meet.google.com/abc-defg-hij",
  "meeting_id": "event_id_here",
  "event_id": "event_id_here",
  "conference_id": "conference_id_here",
  "summary": "Generated Meeting",
  "start_time": "2024-01-01T12:00:00Z",
  "end_time": "2024-01-01T13:00:00Z",
  "calendar_link": "https://calendar.google.com/calendar/event?eid=...",
  "error": null
}
```

## How It Works

### Calendar API Approach

Since Google Meet API requires domain-wide delegation (admin privileges), we use **Google Calendar API** instead:

1. **Create Calendar Event**: Bot creates a calendar event with Google Meet integration
2. **Extract Meet Link**: Google automatically generates a Meet link for the event
3. **Return Link**: Bot extracts and returns the Meet URL

### Benefits

- ✅ **No admin privileges required**
- ✅ **Works with standard Service Account**
- ✅ **Reliable and officially supported**
- ✅ **Generates unique meeting rooms**

### API Endpoints

- `GET /ping` - Health check
- `GET /auth/test` - Test Google authentication
- `POST /create-meet-link` - Create new Google Meet link
- `GET /meet/{event_id}` - Get meeting information

## Troubleshooting

### Common Issues

1. **403 accessNotConfigured**
   - Solution: Enable Google Calendar API in Cloud Console
   - Wait a few minutes after enabling

2. **403 Permission denied**
   - Solution: Check Service Account permissions
   - Ensure correct roles are assigned

3. **Service account file not found**
   - Solution: Check file path in `.env`
   - Verify file permissions (should be 600)

4. **Invalid credentials**
   - Solution: Re-download Service Account JSON
   - Check if project ID matches

### Enable Calendar API

If you see "Google Calendar API has not been used" error:

1. Go to: https://console.developers.google.com/apis/api/calendar-json.googleapis.com/overview?project=YOUR_PROJECT_ID
2. Click "Enable"
3. Wait 2-5 minutes
4. Retry the request

### Debugging

Enable debug logging in `.env`:
```bash
DEBUG=true
LOG_LEVEL=DEBUG
```

Check logs for detailed error information.

## Security Notes

- **Never commit** service account JSON files to git
- **Use secure file permissions** (600) for credentials
- **Rotate service account keys** regularly
- **Use environment variables** for sensitive configuration

## Next Steps

After successful backend setup:
1. Set up Telegram Bot (Task 2.5)
2. Implement inline query handler (Task 2.6)
3. Connect bot with backend (Task 2.7)
4. Test end-to-end functionality 