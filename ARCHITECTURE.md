# System Architecture (Draft)

<!-- This document outlines the PROPOSED architecture -->
<!-- Will be updated as research resolves unknowns -->

---

## High-Level Overview

```
┌─────────────────────────────────────────────────────────┐
│                     USER INTERFACES                      │
├─────────────────┬──────────────────┬────────────────────┤
│  Web Browser    │   iOS Shortcut   │   Voice Device     │
│  (WiFi Device)  │   (iPhone)       │   (Future)         │
└────────┬────────┴────────┬─────────┴──────────┬─────────┘
         │                 │                    │
         │ HTTP            │ HTTP POST          │ HTTP POST
         │                 │                    │
         ▼                 ▼                    ▼
┌─────────────────────────────────────────────────────────┐
│              RASPBERRY PI WEB SERVER                     │
│                                                          │
│  ┌────────────────────────────────────────────────┐    │
│  │          Web Framework (FastAPI/Flask)         │    │
│  │  ┌──────────┬──────────┬──────────┬─────────┐ │    │
│  │  │Dashboard │   API    │  Voice   │  Email  │ │    │
│  │  │  Routes  │ Routes   │ Handler  │ Reader  │ │    │
│  │  └──────────┴──────────┴──────────┴─────────┘ │    │
│  └────────────────────────────────────────────────┘    │
│                         │                               │
│                         ▼                               │
│  ┌────────────────────────────────────────────────┐    │
│  │         Data Layer (SQLite / JSON files)       │    │
│  │  - TODOs                                       │    │
│  │  - Shopping Lists (2 types)                   │    │
│  │  - Cached Emails                              │    │
│  │  - Calendar Events Cache                      │    │
│  └────────────────────────────────────────────────┘    │
└───────────────────────┬─────────────────────────────────┘
                        │
                        │ API Calls (periodic background jobs)
                        ▼
┌─────────────────────────────────────────────────────────┐
│                  EXTERNAL SERVICES                       │
├──────────────────┬──────────────────┬───────────────────┤
│   Gmail API      │  Google Calendar │  Speech-to-Text   │
│   (OAuth2)       │     (OAuth2)     │   (if cloud)      │
└──────────────────┴──────────────────┴───────────────────┘
```

---

## Component Breakdown

### 1. Web Server (Raspberry Pi)
**Technology**: Python + FastAPI (tentative)  
**Responsibilities**:
- Serve dashboard HTML/CSS/JS
- Provide REST API for data operations
- Handle OAuth2 authentication for Gmail/Calendar
- Background jobs for fetching emails/events
- Process voice commands from external devices

**Key Endpoints** (examples):
```python
# Dashboard
GET  /                          # Main dashboard page

# TODOs
GET  /api/todos                 # Get today's TODOs
POST /api/todos                 # Add new TODO
PUT  /api/todos/{id}            # Update TODO (complete/uncomplete)

# Shopping Lists
GET  /api/shopping/groceries    # Get grocery list
POST /api/shopping/groceries    # Add item to grocery list
DELETE /api/shopping/groceries/{id}

GET  /api/shopping/other        # Non-grocery list
# ... similar CRUD operations

# Emails
GET  /api/emails                # Get cached unread emails
GET  /api/emails/{id}           # Get full email content (read-only)
POST /api/emails/refresh        # Manually trigger email fetch

# Calendar
GET  /api/calendar/today        # Today's events
GET  /api/calendar/upcoming     # Events 3-5 days out

# Voice Input
POST /api/voice/command         # Receive voice command from external device
# Body: {"command": "add milk to grocery list"}
```

---

### 2. Frontend (Dashboard UI)
**Technology**: Plain HTML + Alpine.js or React (TBD)  
**Features**:
- Responsive layout for various screen sizes
- Auto-refresh for new data (polling or SSE)
- Simple forms for manual data entry
- Click-to-read email preview

**Example Layout**:
```
┌─────────────────────────────────────────────┐
│  Personal Dashboard      [Refresh] [☰ Menu] │
├─────────────────────────────────────────────┤
│                                             │
│  📧 Unread Emails (3)                       │
│  ┌─────────────────────────────────────┐   │
│  │ • John Doe - Meeting tomorrow       │   │
│  │ • Newsletter - Weekly digest        │   │
│  │ • Jane Smith - Re: Project update   │   │
│  └─────────────────────────────────────┘   │
│                                             │
│  ✓ Today's TODOs                    [+ Add] │
│  ┌─────────────────────────────────────┐   │
│  │ ☐ Buy groceries                     │   │
│  │ ☑ Call dentist                      │   │
│  └─────────────────────────────────────┘   │
│                                             │
│  🛒 Shopping Lists                          │
│  ┌──────────────┬─────────────────────┐   │
│  │ Groceries    │ Other               │   │
│  │ • Milk       │ • Light bulbs       │   │
│  │ • Bread      │                     │   │
│  └──────────────┴─────────────────────┘   │
│                                             │
│  📅 Today's Events                          │
│  ┌─────────────────────────────────────┐   │
│  │ 2:00 PM - Team Meeting              │   │
│  └─────────────────────────────────────┘   │
│                                             │
│  📅 Upcoming (Feb 22-24)                    │
│  ┌─────────────────────────────────────┐   │
│  │ Feb 22: Doctor appointment          │   │
│  └─────────────────────────────────────┘   │
└─────────────────────────────────────────────┘
```

---

### 3. Data Storage
**Option 1: SQLite** (Recommended)
```sql
-- Tables structure example

CREATE TABLE todos (
    id INTEGER PRIMARY KEY,
    text TEXT NOT NULL,
    completed BOOLEAN DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE shopping_items (
    id INTEGER PRIMARY KEY,
    category TEXT CHECK(category IN ('grocery', 'other')),
    name TEXT NOT NULL,
    added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE cached_emails (
    id TEXT PRIMARY KEY,  -- Gmail message ID
    subject TEXT,
    sender TEXT,
    snippet TEXT,
    received_date TIMESTAMP,
    read_in_dashboard BOOLEAN DEFAULT 0,
    cached_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE calendar_events (
    id TEXT PRIMARY KEY,  -- Google Calendar event ID
    title TEXT,
    start_time TIMESTAMP,
    end_time TIMESTAMP,
    description TEXT,
    cached_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

**Option 2: JSON Files** (Simpler, less structured)
```
data/
  todos.json
  shopping_grocery.json
  shopping_other.json
  emails_cache.json
  calendar_cache.json
```

---

### 4. Background Jobs
**Purpose**: Periodically fetch data from external APIs

**Implementation Options**:
- Python `schedule` library
- `APScheduler` for FastAPI
- systemd timers (external to app)

**Jobs**:
```python
# Example job schedule
@scheduler.scheduled_job('interval', minutes=10)
def fetch_emails():
    """Fetch unread emails from last 20 days"""
    # Call Gmail API
    # Update cached_emails table
    # Delete emails older than 20 days from cache

@scheduler.scheduled_job('interval', minutes=30)
def fetch_calendar():
    """Fetch today's events and upcoming 3-5 days"""
    # Call Google Calendar API
    # Update calendar_events table
```

---

### 5. Voice Command Processing
**Flow**:
```
1. External device (iPhone Shortcut) sends POST request
   → /api/voice/command
   → Body: {"text": "add milk to grocery list"}

2. Backend parses command using simple regex or NLP
   → Identify: action (add), item (milk), list (grocery)

3. Execute action
   → INSERT INTO shopping_items (category, name) VALUES ('grocery', 'milk')

4. Return success response
   → {"success": true, "message": "Added milk to grocery list"}
```

**Command Patterns** (examples):
```python
# Simple regex-based parser initially
commands = {
    r"add (.*) to (grocery|other) list": add_shopping_item,
    r"add todo (.*)": add_todo,
    r"mark (.*) as complete": complete_todo,
}
```

---

## Security Considerations

1. **OAuth2 Tokens**: Store in encrypted file or environment variables
2. **Web UI Access**: Consider HTTP Basic Auth for WiFi access
3. **HTTPS**: Use self-signed cert for local network (optional)
4. **Firewall**: Ensure Pi doesn't expose services to internet

---

## Deployment Model

```bash
# Raspberry Pi setup (example)
/home/pi/dashboard/
  ├── app/
  │   ├── main.py              # FastAPI app
  │   ├── models.py            # Data models
  │   ├── routers/
  │   │   ├── todos.py
  │   │   ├── shopping.py
  │   │   ├── emails.py
  │   │   └── calendar.py
  │   └── services/
  │       ├── gmail.py         # Gmail API integration
  │       └── gcal.py          # Calendar API integration
  ├── static/                  # CSS, JS, images
  ├── templates/               # HTML templates
  ├── data/                    # SQLite DB or JSON files
  ├── .env                     # API credentials (gitignored)
  ├── requirements.txt
  └── run.sh                   # Startup script

# Run on boot via systemd service
```

---

## Open Architecture Questions

<!-- To be resolved during research phase -->

- [ ] Should we use Server-Sent Events or polling for real-time updates?
- [ ] Caching strategy: How long to keep email content cached?
- [ ] Error handling: What to display if Gmail API is down?
- [ ] Multi-user support: Single user or support multiple household members?
- [ ] Display device: Will dashboard be viewed on dedicated screen or phones/tablets?

---

## Next Steps
1. Complete RESEARCH.md items
2. Choose specific technologies based on research findings
3. Build minimal prototype (Phase 1 from PHASES.md)
4. Iterate based on real-world testing
