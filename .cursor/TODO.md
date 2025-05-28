# Bot User Story

The user wants to create an inline Telegram bot. Here's how it should work from the user's perspective:

1.  The user, in any chat (group or direct message), types the bot's inline name (e.g., `@meet_the_bot`).
2.  The bot immediately offers an inline suggestion (e.g., "Create a new Google Meet link").
3.  When the user clicks/selects this suggestion, the bot sends a direct, ready-to-use Google Meet link (e.g., `https://meet.google.com/xyz-abcd-efg`) into the chat.
4.  This link should open a brand new, unique Google Meet room.
5.  No calendar integration or other complex features are required; the core functionality is the instant generation and provision of a direct meeting link.

---

# Google Meet Telegram Bot - Code Development Tasks

## Phase 2: Code Writing (Development of Bot and Backend Functionality)

- [x] **Task 2.0: Initialize and Connect to Git Repository** ✅
    - Initialize a Git repository in your local project directory if you haven't already (`git init`).
    - Add the remote repository: `git remote add origin https://github.com/Elevencode/meet_the_bot.git` (or ensure it's set as the origin).
    - Create a `.gitignore` file (add `.env`, `*.json` keyfiles, `__pycache__/`, `venv/` or other virtual environment folders, etc.).
    - Make an initial commit with the project structure and push to the `main` or `master` branch (e.g., `git push -u origin main`).

### Backend Service
- [x] **Task 2.1: Basic Backend Service Setup** ✅
    - Choose framework (e.g., Python + FastAPI).
    - Create backend project structure.
    - Implement a simple health check endpoint (e.g., GET `/ping`).
- [x] **Task 2.2: Backend Integration with Google Meet API - Authentication** ✅
    - Using `google-api-python-client` and the service account JSON key, implement logic in the backend to obtain an authenticated client for the Google Meet API.
- [ ] **Task 2.3: Backend Integration with Google Meet API - Meeting Creation**
    - Implement a function in the backend that uses the authenticated client to call the Google Meet REST API method for creating a "meeting space".
    - Parse the API response to extract the `meetingUri`.
    - Implement basic error handling for Google API responses.
- [ ] **Task 2.4: Create API Endpoint on Backend for Telegram Bot**
    - Create an API endpoint on the Backend service (e.g., POST `/create-meet-link`).
    - This endpoint should call the `create_google_meet_link()` function and return the obtained link (or error) in JSON format.

### Telegram Bot
- [ ] **Task 2.5: Basic Telegram Bot Setup**
    - Choose framework (e.g., `aiogram`).
    - Set up the basic bot structure, connecting to Telegram using the API token.
    - Implement a simple command handler (e.g., `/start`).
- [ ] **Task 2.6: Implement Inline Query Handler in Telegram Bot**
    - Set up a handler for `InlineQuery`.
- [ ] **Task 2.7: Connect Telegram Bot with Backend Service**
    - In the Telegram bot's inline query handler, implement an HTTP client to send a request to the Backend service's API endpoint.
    - Receive the response from the Backend (meeting link or error).
- [ ] **Task 2.8: Format and Send Inline Query Results by Telegram Bot**
    - Upon receiving the link from the Backend, format an `InlineQueryResultArticle` object.
    - Populate fields: `id`, `title`, `input_message_content`.
    - Respond to the inline query with this result.

### General Code Tasks
- [ ] **Task 2.9: Manage Configuration and Secrets in Code**
    - Ensure all sensitive data (Telegram token, path to Google JSON key, backend service URL) is loaded from environment variables or configuration files.
- [ ] **Task 2.10: Error Handling and Logging (Basic)**
    - Implement basic error handling at key stages.
    - Add logging for debugging purposes. 