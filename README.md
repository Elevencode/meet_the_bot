# Google Meet Telegram Bot

An inline Telegram bot that instantly generates Google Meet links for quick video conferences.

## Features

- **Inline Bot**: Type `@meet_the_bot` in any chat to get a Google Meet link
- **Instant Generation**: Creates unique Google Meet rooms on demand
- **Simple Usage**: No calendar integration or complex setup required
- **Direct Links**: Ready-to-use meeting links sent directly to chat

## How It Works

1. User types the bot's inline name (e.g., `@meet_the_bot`) in any chat
2. Bot offers an inline suggestion: "Create a new Google Meet link"
3. User selects the suggestion
4. Bot sends a direct, ready-to-use Google Meet link to the chat
5. Link opens a brand new, unique Google Meet room

## Project Structure

```
meet_the_bot/
├── backend/          # FastAPI backend service
├── bot/             # Telegram bot implementation
├── .env.example     # Environment variables template
├── requirements.txt # Python dependencies
└── README.md       # This file
```

## Setup

### Prerequisites

- Python 3.8+
- Telegram Bot Token (from @BotFather)
- Google Cloud Project with Meet API enabled
- Service Account JSON key for Google API

### Installation

1. Clone the repository:
```bash
git clone https://github.com/Elevencode/meet_the_bot.git
cd meet_the_bot
```

2. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your credentials
```

### Configuration

Create a `.env` file with the following variables:

```env
TELEGRAM_BOT_TOKEN=your_telegram_bot_token
GOOGLE_SERVICE_ACCOUNT_PATH=path/to/service-account.json
BACKEND_URL=http://localhost:8000
```

## Usage

### Running the Backend Service

```bash
cd backend
python main.py
```

The backend will be available at `http://localhost:8000`

### Running the Telegram Bot

```bash
cd bot
python main.py
```

## API Endpoints

### Backend Service

- `GET /ping` - Health check endpoint
- `POST /create-meet-link` - Creates a new Google Meet link

## Development

### Phase 1: Setup ✅
- [x] Initialize Git repository
- [x] Create project structure
- [x] Set up .gitignore

### Phase 2: Backend Development
- [ ] Basic FastAPI service setup
- [ ] Google Meet API integration
- [ ] Authentication with service account
- [ ] Meeting creation endpoint

### Phase 3: Telegram Bot Development
- [ ] Basic bot setup with aiogram
- [ ] Inline query handler
- [ ] Backend service integration
- [ ] Response formatting

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

This project is licensed under the MIT License. 