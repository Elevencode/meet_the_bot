# Setup Instructions

## Google Service Account Configuration

### 1. Create Service Account in Google Cloud Console

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing one
3. Enable Google Meet API:
   - Go to APIs & Services > Library
   - Search for "Google Meet API"
   - Click "Enable"
4. Create Service Account:
   - Go to APIs & Services > Credentials
   - Click "Create Credentials" > "Service Account"
   - Fill in the details and create
5. Generate JSON Key:
   - Click on the created service account
   - Go to "Keys" tab
   - Click "Add Key" > "Create new key" > "JSON"
   - Download the JSON file

### 2. Secure Storage of Credentials

**IMPORTANT: Never commit credentials to the repository!**

1. Create credentials directory outside the repository:
   ```bash
   mkdir -p ~/credentials/meet_the_bot
   ```

2. Move your downloaded JSON file to:
   ```bash
   ~/credentials/meet_the_bot/service-account.json
   ```

3. Set proper permissions:
   ```bash
   chmod 600 ~/credentials/meet_the_bot/service-account.json
   ```

### 3. Environment Configuration

1. Copy the example environment file:
   ```bash
   cp env.example .env
   ```

2. Update `.env` with your actual paths:
   ```bash
   # Update the path to your service account JSON
   GOOGLE_SERVICE_ACCOUNT_PATH=/Users/your_username/credentials/meet_the_bot/service-account.json
   
   # Add your Telegram bot token when ready
   TELEGRAM_BOT_TOKEN=your_actual_bot_token
   ```

### 4. Test the Setup

1. Install dependencies:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. Start the backend:
   ```bash
   cd backend
   python main.py
   ```

3. Test authentication:
   ```bash
   curl http://localhost:8000/auth/test
   ```

   You should see:
   ```json
   {
     "authenticated": true,
     "service_account_file_exists": true,
     "credentials_loaded": true,
     "meet_client_created": true,
     "error": null
   }
   ```

4. Test meeting creation:
   ```bash
   curl -X POST http://localhost:8000/create-meet-link
   ```

## Security Best Practices

- ✅ Service account JSON is stored outside repository
- ✅ `.env` file is in `.gitignore`
- ✅ Proper file permissions set (600)
- ✅ No credentials in code or config files
- ✅ Environment variables used for configuration

## Troubleshooting

### Authentication Issues
- Check if service account JSON file exists and is readable
- Verify the path in `.env` is correct
- Ensure Google Meet API is enabled in your project
- Check service account has necessary permissions

### API Errors
- Verify your Google Cloud project has billing enabled
- Check API quotas and limits
- Review service account permissions 