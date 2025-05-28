# Google Meet Telegram Bot - Setup Instructions

This guide helps you set up the Google Meet Telegram Bot backend service.

## Prerequisites

- Python 3.8 or higher
- Telegram Bot Token

## Simple Setup (No Google Cloud Required!)

This bot now uses a **simple URL generation approach** that doesn't require Google Cloud setup, API keys, or special permissions. It generates standard Google Meet links that work just like regular Meet rooms.

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

# Telegram Bot Configuration
TELEGRAM_BOT_TOKEN=your_telegram_bot_token_here
```

### 5. Test Setup

```bash
cd backend
python main.py
```

In another terminal, test the service:

```bash
# Health check
curl http://localhost:8000/ping

# Create Google Meet link
curl -X POST http://localhost:8000/create-meet-link

# Get meeting info
curl http://localhost:8000/meet/abc-defg-hij
```

Expected response for creating a meeting:
```json
{
  "success": true,
  "meeting_uri": "https://meet.google.com/abc-defg-hij",
  "meeting_code": "abc-defg-hij",
  "summary": "Generated Meeting",
  "description": "Click the meeting link to join the Google Meet room...",
  "instructions": {
    "how_to_join": "Click the meeting link or go to meet.google.com and enter the code",
    "meeting_code": "abc-defg-hij",
    "note": "The meeting room will be created automatically when someone joins"
  }
}
```

## How It Works

### Simple URL Generation Approach

The bot generates **standard Google Meet URLs** using the format `https://meet.google.com/xxx-xxxx-xxx`:

1. **Generate Unique Code**: Creates a random meeting code in Google Meet format
2. **Return Meeting Link**: Provides a working Google Meet URL
3. **Auto-Room Creation**: When first person joins, Google automatically creates the meeting room

### Benefits

- ✅ **No Google Cloud setup required**
- ✅ **No API keys or authentication needed**
- ✅ **No admin privileges required**
- ✅ **Works immediately after setup**
- ✅ **Generates real Google Meet links**
- ✅ **Rooms created automatically when accessed**

### API Endpoints

- `GET /ping` - Health check
- `POST /create-meet-link` - Create new Google Meet link
- `GET /meet/{meeting_code}` - Get meeting information

## Advanced Usage

### Custom Meeting Parameters

You can create meetings with custom titles and durations:

```bash
curl -X POST -H "Content-Type: application/json" \
  -d '{"summary":"Team Meeting","description":"Weekly sync","duration_minutes":30}' \
  http://localhost:8000/create-meet-link
```

### Integration with Telegram Bot

The backend is designed to work with a Telegram inline bot:

1. User types `@meet_the_bot` in any chat
2. Bot calls `POST /create-meet-link` API
3. Bot responds with inline result containing the Google Meet link
4. User selects the result to share the meeting link in chat

## Next Steps

After successful backend setup:
1. Set up Telegram Bot (Task 2.5)
2. Implement inline query handler (Task 2.6)
3. Connect bot with backend (Task 2.7)
4. Test end-to-end functionality

## Troubleshooting

### Common Issues

1. **Port already in use**
   - Solution: Change PORT in `.env` or stop other services on port 8000

2. **Module not found errors**
   - Solution: Ensure virtual environment is activated and dependencies installed

3. **Permission errors**
   - Solution: Check file permissions and virtual environment setup

### Testing Generated Links

To verify that generated links work:
1. Copy a generated meeting URL (e.g., `https://meet.google.com/abc-defg-hij`)
2. Open it in your browser
3. You should see the Google Meet interface
4. The room will be created when you join

### Debugging

Enable debug logging in `.env`:
```bash
DEBUG=true
LOG_LEVEL=DEBUG
```

Check logs for detailed information about link generation and API requests.

## Security Notes

- **No sensitive credentials required**
- **No API keys to manage**
- **Safe URL generation using random codes**
- **Standard Google Meet security applies to generated rooms** 