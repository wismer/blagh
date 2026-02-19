# Context for AI Assistants

<!-- This file helps AI understand the project quickly in future sessions -->
<!-- Update this as the project evolves -->

---

## What This Project Is
A **personal dashboard for a Raspberry Pi** that displays daily essential info (emails, TODOs, shopping lists, calendar) with multi-modal input (web UI + voice commands via iOS).

**Current Status**: Phase 0 - Research & Planning  
**Last Updated**: February 19, 2026

---

## Key Constraints
1. **Token Efficiency**: Minimize redundant explanations via documentation
2. **Incremental Development**: No feature is built until prerequisites are validated
3. **Research-First**: Critical unknowns must be resolved before coding (see RESEARCH.md)
4. **Local-First**: Raspberry Pi hosts everything; WiFi-only access

---

## Project Files (Read These First)
- **PROJECT.md**: Vision, features, open questions
- **RESEARCH.md**: Unknowns that need investigation (current work)
- **ARCHITECTURE.md**: Proposed technical design
- **PHASES.md**: Development roadmap with phase gates

---

## Technology Stack (Tentative)
- **Backend**: Python + FastAPI (pending final decision in Phase 0)
- **Frontend**: Plain HTML + Alpine.js (lightweight, no build step)
- **Database**: SQLite (simple, embedded)
- **APIs**: Gmail API, Google Calendar API (OAuth2)
- **Voice Input**: iOS Shortcuts → HTTP POST (MVP), may add dedicated hardware later

---

## Critical Open Questions (Blockers)
See RESEARCH.md for details, but key unknowns:
1. Gmail API rate limits and OAuth2 flow for local app ❓
2. Best voice input approach (iOS Shortcut vs. dedicated hardware) ❓
3. Security model for WiFi-only web access ❓

---

## Design Decisions Made
<!-- Document important choices to avoid revisiting -->

### ✅ Decided:
- **No cloud hosting**: Everything runs locally on Raspberry Pi
- **Read-only emails**: Dashboard won't support composing/sending
- **WiFi-only access**: No internet-facing exposure
- **Incremental phases**: Build basic features before advanced ones

### ❌ Explicitly NOT Doing (for now):
- Multi-user/family accounts
- Mobile native apps (web UI only)
- Email composition/sending from dashboard
- Smart home integrations
- Fancy animations or complex UI

---

## Code Patterns to Follow
<!-- Add these as project develops -->

### File Structure:
```
raspberry-pi-dashboard/
  ├── app/
  │   ├── main.py              # FastAPI entry point
  │   ├── models.py            # Data models (SQLAlchemy or Pydantic)
  │   ├── database.py          # DB connection & operations
  │   ├── routers/             # API route modules
  │   └── services/            # External API integrations (Gmail, Calendar)
  ├── static/                  # CSS, JS, images
  ├── templates/               # Jinja2 templates
  ├── data/                    # SQLite database (gitignored)
  ├── tests/                   # Unit & integration tests
  ├── .env                     # API credentials (gitignored)
  ├── requirements.txt
  └── README.md                # Setup instructions
```

### Database Schema (Draft):
```sql
-- See ARCHITECTURE.md for full schema
-- Keep it simple, optimize later
```

### API Endpoint Patterns:
```python
# RESTful conventions
GET    /api/todos          # List
POST   /api/todos          # Create
PUT    /api/todos/{id}     # Update
DELETE /api/todos/{id}     # Delete

# Voice commands (special case)
POST   /api/voice/command  # Natural language processing
```

---

## Common Pitfalls to Avoid
<!-- Learn from mistakes, document them here -->

1. **Don't build features before validating feasibility** (e.g., Gmail API might have unexpected limits)
2. **Don't optimize prematurely** (SQLite is fine until it's not)
3. **Don't hard-code credentials** (use environment variables)
4. **Don't skip testing on actual Raspberry Pi** (performance differences matter)

---

## How to Use This Project with AI

### Starting a New Session:
```
"I'm working on the Raspberry Pi dashboard project. 
Please read CLAUDE.md and [relevant file] for context.
I need help with [specific task from PHASES.md]."
```

### When Asking Questions:
- ✓ Reference specific files and line numbers
- ✓ Include error messages verbatim
- ✓ State what you've already tried
- ✓ Mention which phase you're in (from PHASES.md)

### After Making Progress:
Update relevant docs (PROJECT.md, RESEARCH.md, PHASES.md, this file) so next session has fresh context.

---

## External Resources
<!-- Links to helpful documentation -->

- Gmail API: https://developers.google.com/gmail/api
- Google Calendar API: https://developers.google.com/calendar/api
- FastAPI Docs: https://fastapi.tiangolo.com
- Raspberry Pi Setup: https://www.raspberrypi.com/documentation/
- iOS Shortcuts: https://support.apple.com/guide/shortcuts/welcome/ios

---

## What to Ask Me (User)
If you (AI) need clarification:
- **Functional questions**: "Should emails older than 20 days be deleted or archived?"
- **Priority questions**: "Is voice input a must-have or nice-to-have?"
- **Constraint questions**: "What Raspberry Pi model are you using?"

Don't guess - ask!

---

## Current Phase Details

### Phase 0: Research & Planning (ACTIVE)
**Goal**: Answer all HIGH-priority questions in RESEARCH.md before writing any code.

**Next Immediate Steps**:
1. Research Gmail API (RESEARCH.md #1)
2. Test OAuth2 flow with sample Python script
3. Research Google Calendar API (RESEARCH.md #3)
4. Finalize technology stack choice (RESEARCH.md #5)

**What I (user) am working on now**:
<!-- Update this as you make progress -->
- Reading documentation for Gmail API
- Setting up Google Cloud project for API credentials
- Testing OAuth2 flow with example code

**Blockers**:
<!-- Note anything preventing progress -->
- None yet (just started)

---

## Session Notes
<!-- Quick notes for continuity between AI sessions -->

**2026-02-19**: 
- Created initial project structure (PROJECT.md, RESEARCH.md, ARCHITECTURE.md, PHASES.md)
- Defined phases and token-efficient workflows
- Ready to begin research phase

<!-- Add dated notes as project progresses -->
