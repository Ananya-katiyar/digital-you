# Digital You — Daily Progress Log

## Phase 1 — Foundation & Auth

### Day 0 — Apr 8, 2026
- Created GitHub repo
- Set up folder structure (frontend, backend, docs)
- Added .gitignore and .env.example
- First commit pushed

### Day 1 — Apr 9, 2026
- Set up Python virtual environment
- Installed FastAPI + Uvicorn
- Created main.py with health check route GET /ping
- Server running on localhost:8000
- Swagger UI working at /docs

### Day 2 — Apr 10, 2026
- Installed Motor (async MongoDB driver)
- Created MongoDB Atlas free cluster
- Built async database connection with lifecycle hooks
- Fixed SSL issue with certifi
- GET /db-check endpoint returning 200 OK

### Day 3 — Apr 11, 2026
- Created Google Cloud project
- Enabled Gmail API and Google Calendar API
- Configured OAuth 2.0 consent screen
- Built GET /auth/google and GET /auth/callback routes
- Full OAuth login flow tested and working

### Day 4 — Apr 12, 2026
- Installed cryptography package
- Generated Fernet secret key
- Built encryption.py with encrypt/decrypt functions
- Created user document schema with preferences
- Tokens encrypted and stored in MongoDB Atlas
- Verified encrypted data in Atlas Data Explorer

### Day 5 — Apr 13, 2026
- Built gmail.py service with token refresh logic
- Built calendar.py service for next 7 days events
- Created GET /emails/ returning real Gmail inbox
- Created GET /calendar/events returning calendar data
- All routes grouped and visible in Swagger UI

### Day 6 — Apr 14, 2026
- Created Pydantic models for profile validation
- Built GET /profile/ and PATCH /profile/ routes
- Rule engine foundation in place
- Wrote 3 pytest tests — all passing
- Implemented mocking pattern for DB tests

### Day 7 — Apr 15, 2026
- End-to-end integration test — all 5 endpoints 200 OK
- Updated README.md with full setup instructions
- Created PROGRESS.md daily log
- Tagged v0.1.0-week1 milestone on GitHub
- Week 1 complete!

## Phase 2 — NLP & Risk Engine

### Day 8 — Apr 16, 2026
- Installed spaCy + en_core_web_sm model
- Created nlp.py with detect_intent() function
- 4 intent classes: casual, scheduling, urgent, promotional
- Keyword + pattern matching — fully offline, no API calls
- Manual test on 5 samples — all correct
- Tagged and committed feat: add NLP intent detection with spaCy

### Day 9 — Apr 17, 2026
- Installed sumy for offline text summarisation
- Extended nlp.py with extract_entities() using spaCy NER
- Added summarise_text() using LexRank algorithm
- Added analyse_email() returning { intent, entities, summary }
- Wired NLP analysis into GET /emails/ route
- Fixed keyword collision bug: 'free' was matching promotional
- Tagged and committed feat: entity extraction and email summarisation

### Day 10 — Apr 18, 2026
- Installed Ollama + pulled Mistral 7B model (local, free, offline)
- Installed LangChain + langchain-ollama + langchain-core
- Created llm.py with generate_draft_reply() using PromptTemplate | LLM chain
- Created POST /drafts/ endpoint
- Draft correctly generated: professional, non-committal, no placeholders
- Updated requirements.txt
- Tagged and committed feat: LangChain + Ollama LLM reply draft generation

### Day 11 — Apr 19, 2026
- Created risk.py with classify_risk() function
- Three risk levels: low / medium / high with corresponding actions
- High risk keywords: financial, legal, HR, security, medical
- Intent-based fallback classification
- User rule engine: check_user_rules() applies personal overrides
- Wired risk classification into GET /emails/ route
- Tagged and committed feat: rule-based risk classification engine

### Day 12 — Apr 20, 2026
- Upgraded rules from strings to structured UserRule Pydantic model
- rule_type, condition, action fields — typed and validated
- Updated check_user_rules() to handle structured rules
- Created decisions.py service for audit trail logging
- Created decisions MongoDB collection
- Built GET /decisions/ and PATCH /decisions/{id}/reviewed routes
- Tagged and committed feat: user rule engine and decision logging to MongoDB

### Day 13 — Apr 21, 2026
- Created queue.py service with add_to_queue() and resolve_queue_item()
- Duplicate check before queuing — prevents flooding
- Created pending_actions MongoDB collection
- Built GET /queue/, POST /queue/, POST /queue/{id}/approve, POST /queue/{id}/reject
- Wired queue + decision logging into GET /emails/ pipeline
- AFK mode integration — queues all non-low risk when user is away
- Tagged and committed feat: approval queue with approve/reject endpoints

### Day 14 — Apr 22, 2026
- Created tests/test_nlp_risk.py with 19 tests
- Coverage: intent detection (7), risk classification (8), rule engine (4)
- All edge cases covered including the 'free' keyword regression test
- Dependency injection pattern used for time-based rule testing
- 19/19 tests passing in 13.09 seconds
- Tagged and committed test: NLP intent, risk engine, and rule engine edge cases

### Day 15 — Apr 23, 2026
- Created tests/test_integration_week2.py
- Full pipeline tests: NLP → risk → correct output verified
- All Week 1 + Week 2 endpoints confirmed working
- Updated README.md with Week 2 endpoints and architecture
- Updated PROGRESS.md
- Tagged v0.2.0-week2 milestone on GitHub
- Week 2 complete!

## Phase 3 — Frontend Dashboard
- React / Next.js dashboard
- Email inbox with risk badges
- Approval queue UI
- Decision log viewer
- Profile + rule management