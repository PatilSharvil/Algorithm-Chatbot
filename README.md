# DSA Algorithm Explanation Chatbot

This is a Flask-based chatbot application that uses Google's Gemini API to provide algorithmic explanations and approaches for DSA problems. The application includes a history panel for accessing past conversations and uses MongoDB for data storage, along with NumPy and Pandas for data analysis.

## Features

- Text-based interface for inputting DSA problems
- Algorithmic approach explanations using Google Gemini API
- Focus on explaining time/space complexity and data structures
- Step-by-step approach explanation without full code solutions
- History panel for accessing past conversations (like ChatGPT/Gemini)
- MongoDB database for storing conversations and user sessions
- Data analysis using NumPy and Pandas

## Tech Stack

- Python 3.8+
- Flask
- Google Generative AI SDK
- MongoDB
- PyMongo
- NumPy
- Pandas
- HTML/CSS/JavaScript
- Bootstrap 5

## Setup and Installation

1. Clone or download the project files
2. Create a virtual environment (optional but recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Get a Google Gemini API key from [Google AI Studio](https://aistudio.google.com/)
5. Rename `.env.example` to `.env` and fill in your configuration:
   ```
   GEMINI_API_KEY=your_gemini_api_key_here
   MONGO_URI=mongodb://localhost:27017/chatbot_db
   SECRET_KEY=your_secret_key_here
   ```
6. Make sure MongoDB is running on your system
7. Run the application:
   ```bash
   python app.py
   ```
8. Open your browser and go to `http://localhost:5000`

## Usage

- Type your DSA problem or question in the input field at the bottom
- The chatbot will provide algorithmic explanations without code
- Access your conversation history in the left sidebar
- Click on any previous conversation to continue from where you left off
- Use the "New Chat" button to start a fresh conversation
- Use the "Clear All" button to delete all conversations

## Data Analysis

The application includes analytics features that use NumPy and Pandas to analyze:

- User engagement patterns
- Message length statistics
- Conversation frequency
- Activity time trends

Analytics can be accessed via the `/api/analytics/usage` endpoint.

## Project Structure

```
chatbot/
├── app/
│   ├── __init__.py
│   ├── models/
│   │   ├── database.py
│   │   └── models.py
│   ├── routes/
│   │   ├── main.py
│   │   ├── history.py
│   │   ├── api.py
│   │   └── analytics.py
│   ├── static/
│   │   └── css/
│   │       └── style.css
│   └── templates/
│       ├── base.html
│       ├── index.html
│       └── history.html
├── app.py
├── requirements.txt
├── .env
└── README.md
```

## API Endpoints

- `GET /` - Main chat interface
- `POST /api/chat` - Send a message and get a response
- `GET /api/conversations` - Get all conversations for a user
- `GET /api/conversation/<id>` - Get a specific conversation with its messages
- `POST /api/new_conversation` - Start a new conversation
- `GET /api/history/conversations` - Get conversation history for the history panel
- `DELETE /api/history/conversation/<id>` - Delete a specific conversation
- `DELETE /api/history/conversations` - Delete all conversations
- `GET /api/analytics/usage` - Get usage analytics

## MongoDB Schema

The application uses three collections:

1. `users` - Stores user information
2. `conversations` - Stores conversation metadata (title, timestamps)
3. `messages` - Stores individual messages within conversations

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request
