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

```
digital-you/
├── backend/
│   └── app/
│       ├── core/        # DB connection, encryption
│       ├── models/      # Pydantic schemas, user documents
│       ├── routes/      # API endpoints
│       └── services/    # Gmail, Calendar business logic
├── frontend/            # Coming Week 3
└── docs/                # Architecture notes
```

## Setup Instructions

### 1. Clone the repo
```bash
git clone https://github.com/Ananya-katiyar/digital-you.git
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
| GET | /emails/ | Fetch + analyse inbox emails |
| GET | /calendar/events | Fetch calendar events |
| GET | /profile/ | Get user preferences |
| PATCH | /profile/ | Update user preferences |
| POST | /drafts/ | Generate LLM draft reply |
| GET | /decisions/ | View risk decision audit trail |
| PATCH | /decisions/{id}/reviewed | Mark decision as reviewed |
| GET | /queue/ | View approval queue |
| POST | /queue/ | Add item to queue |
| POST | /queue/{id}/approve | Approve queued item |
| POST | /queue/{id}/reject | Reject queued item |

## Architecture — Phase 2 NLP & Risk Pipeline
```
Incoming Email
↓
NLP Analysis (spaCy + sumy)
→ intent: casual / scheduling / urgent / promotional
→ entities: names, dates, orgs
→ summary: condensed text
↓
Risk Classification (rule-based)
→ HIGH risk keywords → escalate
→ User rules → override
→ Intent-based → low / medium / high
↓
Decision Logger → MongoDB (audit trail)
↓
┌─────────────────────────────────────────────┐
│                         │                   │
LOW risk              MEDIUM risk         HIGH risk
auto_draft          suggest_and_approve    escalate
→ Approval Queue    → Alert user
```

## Progress Tracker
| Phase | Status |
|-------|--------|
| 1 > Foundation & Auth | ✅ Complete |
| 2 > NLP & Risk Engine | ✅ Complete |
| 3 > Frontend Dashboard | 🔜 Coming |
| 4 > Deployment | 🔜 Coming |