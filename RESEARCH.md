## 1. Gmail API Feasibility
**Status**: [x] Not Started
**Priority**: HIGH (blocking core feature)

### Questions to Answer:
- [x] Can Gmail API retrieve unread emails from last N days?
- [x] What authentication flow is needed for a local Raspberry Pi app?
- [x] What are the rate limits? (queries per day/hour)
- [x] Can we filter by labels, dates, read/unread status?
- [x] Is there a webhook/push notification option, or must we poll?
- [x] Cost implications (if any)?

### Research Method:
```
1. Read Gmail API documentation
2. Create test Google Cloud project
3. Try OAuth2 flow with desktop/installed app credentials
4. Test sample API calls with Python/Node.js
5. Document rate limits and quotas
```

### Findings:
<!-- Document results here after research -->
- Gmail API allows for filtering by date and read status
- Requires OAuth2
- Gmail API Rate limit is very high, and extremely unlikely it would ever be reached. Poll for updates (~10min)
- cost is negligible or non-existent

```
Example:
- Gmail API allows filtering by date and read status ✓
- Requires OAuth2 with "installed app" credentials
- Rate limit: 250 quota units/user/second, 1 billion/day
- Must poll for updates (no push for personal accounts)
- Cost: FREE for personal use
```

---

## 2. Voice Input Architecture
**Status**: [x] Not Started
**Priority**: MEDIUM (can build dashboard without it first)

### Option A: iOS Phone Integration
- [x] Research iOS Shortcuts capabilities
- [x] Can Shortcuts POST to local network IP?
- [x] Does it support wake word detection?
- [ ] Alternative: Custom iOS app with speech-to-text?

### Findings
- an iOS shorcut can be activated with "hey buddy", record my voice "groceries, milk", then make a POST request from my phone to the server (`gremlin.computer/<path>`) with JSON, something like `{"type": "grocery", "item": "milk" }`.
- iOS shortcuts for speech-to-text can break up the contents by word, so this can mean "Hey Buddy, milk, celery, potatoes" would result in `{"type": "groceries", "items": ["milk", "celery", "potatoes"]}`
- More capabilities are present but this is sufficient for my needs. This WILL however mean that we're going to create a web server to handle this using my domain, gremlin.computer.


### Option B: Dedicated Hardware
- [ ] USB microphone directly on Raspberry Pi
- [ ] Wake word detection libraries (Porcupine, Snowboy)
- [ ] Speech-to-text options:
  - Google Cloud Speech-to-Text (cloud, costs money)
  - Whisper (local, resource-intensive)
  - Vosk (local, lightweight)

### Option C: Smart Speaker Hack
- [ ] Can Alexa/Google Home send requests to local server?
- [ ] Custom skills/actions pointing to local IP?

### Recommendation:
<!-- Fill in after research -->
```
Example:
RECOMMENDED: Start with iOS Shortcuts (simplest, no extra hardware)
- Shortcut can POST to http://raspberrypi.local:8080/add-item
- No custom app needed
- Wake word: Use iOS "Hey Siri" trigger
- Fallback: Add USB mic + Vosk for standalone solution
```

---

## 3. Calendar Integration
**Status**: [~] Not Started
**Priority**: HIGH

### Questions:
- [ ] Which calendar service? (Google Calendar, iCloud, CalDAV?)
- [ ] Can we use same OAuth2 flow as Gmail?
- [ ] How to filter events by date range?
- [ ] Rate limits?

### Findings
- This we will do later. But we will need to sync iCloud & Google Calendar for multiple accounts.

---

## 4. Security Model
**Status**: [x] Not Started
**Priority**: MEDIUM (before deploying on network)

### Questions:
- [ ] Is WiFi-only access sufficient, or add password protection?
- [ ] HTTPS needed for local network?
- [ ] Where to store API credentials safely on Pi?
- [ ] Should we implement user accounts, or single-user system?

### Research:
```
- Look into mDNS for easy access (raspberrypi.local)
- Research .env file encryption or system keyring
- Consider simple HTTP Basic Auth for web UI
```

### Findings
- I think the best scenario here is that the rasperry pi will be the webserver for my domain, `gremlin.computer`. This will require some configuration to set it up properly and with authentication. SSL, etc.

---

## 5. Technology Stack Selection
**Status**: [ ] Not Started
**Priority**: HIGH (needed for Phase 1)

### Backend Options:
- [x] **Python + Flask**: Simple, great for Pi, extensive API libraries
- [ ] **Python + FastAPI**: Modern, async, auto-documentation
- [ ] **Node.js + Express**: JavaScript everywhere, good real-time support

### Frontend Options:
- [ ] **Plain HTML/CSS/JS**: Zero build step, fastest
- [x] **React/Vue**: Better for complex state management
- [ ] **Jinja2 templates**: Server-side rendering, simple

### Database:
- [ ] **JSON files**: Simplest, good for small data
- [ ] **SQLite**: Structured, relational, no server needed
- [x] **PostgreSQL**: Overkill but future-proof

### Findings

- For backend, Python + Flask
- for Frontend, React/Vue
- for database, because things might get complicated, postgreSQL

## 6. Database schema

### Findings
- will need a `user` table for authentication purposes
- a table(s) to handle to do's lists
- I want to be able to create a history of all groceries. Sometimes I will go through the list, and then remove them so that they're no longer active. For example, I add milk and celery, I then later go shopping, retrieve the list remotely. When that happens, all "active" groceries can be archived but be tied to an event?
- no need to record email interactions, we will ignore that.
- logging activity might be a good idea for observability purposes


## 6. Raspberry Pi Hardware Requirements
**Status**: [x] Not Started
**Priority**: LOW (most Pis will work)

### Questions:
- [ ] Minimum RAM needed? (probably 1GB+)
- [ ] Storage for emails/cache? (probably 8GB+ SD card)
- [ ] Display output needed, or headless?
- [ ] Power consumption considerations?
