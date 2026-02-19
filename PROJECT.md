# Raspberry Pi Personal Dashboard

## Vision
A locally-hosted dashboard running on a Raspberry Pi that displays daily essential information and allows multi-modal input (UI + voice).

## Core Features

### Display Components
- **Unread Emails**: Gmail messages from the last 20 days
- **Daily TODOs**: Task list for today
- **Shopping Lists**: 
  - Groceries
  - Non-groceries
- **Calendar Events**:
  - Today's events
  - Upcoming events (3-5 days out)

### Input Methods
1. **Web UI**: Accessible from any device on the same WiFi network
2. **Voice Commands**: Speech-to-text for adding items (e.g., "Hey Buddy, add Milk to the grocery list")

### Email Interaction
- Click to read emails directly in dashboard (read-only)
- "Reply" button redirects to Gmail web interface

---

## Known Constraints & Open Questions

### Gmail Integration
<!-- UNKNOWN: Need to verify -->
- ❓ Can we retrieve emails via Gmail API?
- ❓ What are the rate limits?
- ❓ OAuth2 requirements for local app?
- ❓ How to handle multiple Gmail accounts (if needed)?

### Voice Recognition
<!-- CRITICAL DECISION POINT -->
- ❓ iOS phone as voice input device?
- ❓ Requires custom iOS app or can use Shortcuts?
- ❓ Alternative: Dedicated voice device (ESP32, USB mic on Pi)?
- ❓ Wake word detection ("Hey Buddy") - local or cloud service?
- ❓ Speech-to-text API: Google, Whisper, others?

### Security & Access
<!-- MUST RESOLVE BEFORE BUILDING -->
- ❓ Authentication for web UI (WiFi-only sufficient)?
- ❓ HTTPS for local network?
- ❓ API credentials storage on Raspberry Pi?

### Technical Stack
<!-- TO BE DETERMINED -->
- ❓ Backend framework (Flask, FastAPI, Node.js)?
- ❓ Frontend framework (React, Vue, plain HTML/CSS)?
- ❓ Database (SQLite, PostgreSQL, or JSON files)?
- ❓ Real-time updates (polling, WebSockets, Server-Sent Events)?

### Raspberry Pi Specifications
<!-- AFFECTS PERFORMANCE DECISIONS -->
- ❓ Which Pi model? (3, 4, 5, Zero?)
- ❓ RAM limitations?
- ❓ Storage requirements?

---

## Design Principles

1. **Start Simple**: Build minimal viable version first
2. **Offline-First**: Dashboard should work even if external APIs are down
3. **Privacy-Focused**: All data processing local when possible
4. **Token-Efficient Development**: Document decisions to avoid re-explaining project

---

## Current Status
**Phase**: Planning & Research
**Next Steps**: See RESEARCH.md and PHASES.md
