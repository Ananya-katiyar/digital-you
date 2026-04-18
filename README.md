# Digital You — Autonomous AI Agent

An autonomous AI agent that acts as your digital representative. Privacy-first, risk-aware, and human-in-the-loop.

## Tech Stack
- **Backend:** Python + FastAPI
- **Database:** MongoDB (Motor async driver)
- **AI:** LangChain + OpenAI (Week 2+)
- **Auth:** Google OAuth 2.0
- **Encryption:** Fernet (AES-128)
- **Frontend:** React / Next.js (Week 3+)

## Project Structure

digital-you/
├── backend/
│   └── app/
│       ├── core/        # DB connection, encryption
│       ├── models/      # Pydantic schemas, user documents
│       ├── routes/      # API endpoints
│       └── services/    # Gmail, Calendar business logic
├── frontend/            # Coming Week 3
└── docs/                # Architecture notes

## Setup Instructions

### 1. Clone the repo
```bash
git clone https://github.com/YOUR_USERNAME/digital-you.git
cd digital-you/backend
```

### 2. Create virtual environment
```bash
python -m venv venv
venv\Scripts\activate  # Windows
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Set up environment variables
```bash
cp .env.example .env
# Fill in your values in .env
```

### 5. Run the server
```bash
uvicorn app.main:app --reload
```

### 6. Visit API docs
http://localhost:8000/docs

## API Endpoints
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /ping | Health check |
| GET | /db-check | MongoDB connection check |
| GET | /auth/google | Google OAuth login |
| GET | /auth/callback | OAuth callback |
| GET | /emails/ | Fetch inbox emails |
| GET | /calendar/events | Fetch calendar events |
| GET | /profile/ | Get user preferences |
| PATCH | /profile/ | Update user preferences |

## Progress Tracker
| Phase | Status |
|-------|--------|
| Week 1 — Foundation & Auth | ✅ Complete |
| Week 2 — NLP & Risk Engine | 🔜 Coming |
| Week 3 — Frontend Dashboard | 🔜 Coming |
| Week 4 — Deployment | 🔜 Coming |