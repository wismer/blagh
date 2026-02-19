# Development Phases

<!-- Break project into incremental milestones -->
<!-- Each phase should produce a working, testable version -->
<!-- Do NOT proceed to next phase until current phase is validated -->

---

## Phase 0: Research & Planning ⏳ (CURRENT)
**Goal**: Answer critical unknowns before writing code  
**Duration**: 1-2 weeks (part-time)

### Tasks:
- [ ] Research Gmail API feasibility (RESEARCH.md #1)
- [ ] Research Calendar API integration (RESEARCH.md #3)
- [ ] Choose technology stack (RESEARCH.md #5)
- [ ] Design database schema
- [ ] Plan security approach (RESEARCH.md #4)
- [ ] Document findings in this project structure

### Success Criteria:
- ✓ All HIGH-priority research items in RESEARCH.md completed
- ✓ Technology stack selected and documented
- ✓ Confidence that core features are feasible

### Deliverables:
- Updated RESEARCH.md with findings
- Finalized ARCHITECTURE.md
- Ready to start coding Phase 1

---

## Phase 1: Minimal Local Dashboard 🎯
**Goal**: Build basic dashboard with manual data entry only (no external APIs)  
**Duration**: 1 week

### Features:
- [ ] Web server running on localhost (later Raspberry Pi)
- [ ] Single-page dashboard displaying:
  - [ ] TODO list (add, complete, delete)
  - [ ] Grocery shopping list (add, delete)
  - [ ] Other shopping list (add, delete)
- [ ] Data persists across server restarts (SQLite or JSON files)
- [ ] Basic styling (readable and functional)

### NOT in this phase:
- ❌ Gmail integration
- ❌ Calendar integration
- ❌ Voice commands
- ❌ WiFi network access (localhost only)

### Success Criteria:
- ✓ Can add/remove TODOs and shopping items via web UI
- ✓ Data persists after server restart
- ✓ Dashboard loads in under 2 seconds
- ✓ Works on development machine (test before Pi deployment)

### Deliverables:
```
Code structure:
  app/
    main.py              # Web server entry point
    database.py          # SQLite/JSON operations
    templates/
      index.html         # Dashboard page
    static/
      styles.css
      script.js
```

### Testing:
```bash
# Run locally first
python app/main.py
# Open http://localhost:5000
# Add some TODOs and shopping items
# Restart server
# Verify data persists
```

---

## Phase 2: Gmail Integration 📧
**Goal**: Display unread emails from last 20 days  
**Duration**: 3-5 days

### Prerequisites:
- ✓ Phase 1 complete and working
- ✓ Gmail API research done (RESEARCH.md #1)
- ✓ Google Cloud project created with Gmail API enabled
- ✓ OAuth2 credentials obtained

### Features:
- [ ] Authenticate with Gmail API (OAuth2 flow)
- [ ] Background job: Fetch unread emails every 10 minutes
- [ ] Display email list in dashboard (subject, sender, snippet)
- [ ] Click email to view full content in dashboard
- [ ] "Reply in Gmail" button opens Gmail web interface
- [ ] Cache emails locally (avoid excessive API calls)

### Success Criteria:
- ✓ Dashboard shows current unread emails
- ✓ Clicking email displays readable content
- ✓ OAuth2 authentication works (initial setup)
- ✓ Emails auto-refresh without manual intervention
- ✓ Respects Gmail API rate limits

### Technical Decisions Needed:
- [ ] OAuth2 token storage location
- [ ] How to handle expired tokens (auto-refresh)
- [ ] Email caching duration

---

## Phase 3: Calendar Integration 📅
**Goal**: Display today's events and upcoming events (3-5 days)  
**Duration**: 2-3 days

### Prerequisites:
- ✓ Phase 2 complete
- ✓ Google Calendar API research done (RESEARCH.md #3)

### Features:
- [ ] Use same OAuth2 flow as Gmail (shared credentials)
- [ ] Background job: Fetch calendar events every 30 minutes
- [ ] Display "Today's Events" section
- [ ] Display "Upcoming Events" section (3-5 days out)
- [ ] Cache events locally

### Success Criteria:
- ✓ Dashboard shows today's calendar events
- ✓ Upcoming events displayed separately
- ✓ Events refresh automatically
- ✓ Handles all-day events vs. timed events

---

## Phase 4: Network Access & Raspberry Pi Deployment 🥧
**Goal**: Deploy to Raspberry Pi, accessible from WiFi devices  
**Duration**: 1 week

### Prerequisites:
- ✓ Phases 1-3 complete and tested on dev machine
- ✓ Raspberry Pi hardware acquired and set up

### Tasks:
- [ ] Set up Raspberry Pi OS
- [ ] Install Python and dependencies
- [ ] Transfer code to Raspberry Pi
- [ ] Configure server to bind to 0.0.0.0 (all interfaces)
- [ ] Set up systemd service (auto-start on boot)
- [ ] Configure mDNS (access via raspberrypi.local)
- [ ] Test access from phone/laptop on same WiFi

### Security:
- [ ] Add HTTP Basic Authentication
- [ ] Store OAuth2 tokens securely
- [ ] Consider self-signed HTTPS certificate

### Success Criteria:
- ✓ Dashboard accessible from phone via WiFi
- ✓ Server starts automatically on Pi boot
- ✓ Performance acceptable (page loads in <3 seconds)
- ✓ Runs continuously without crashes

### Testing:
```bash
# From phone on same WiFi
http://raspberrypi.local:5000

# Verify all features work:
# - Add/remove TODOs
# - View emails
# - See calendar events
```

---

## Phase 5: Voice Command Integration (iOS Shortcut) 🎤
**Goal**: Add items via iOS Shortcuts and voice  
**Duration**: 2-3 days

### Prerequisites:
- ✓ Phase 4 complete (Pi accessible on network)
- ✓ Voice input research done (RESEARCH.md #2)

### Features:
- [ ] New API endpoint: POST /api/voice/command
- [ ] Simple command parser (regex-based initially)
- [ ] Create iOS Shortcut:
  - Trigger: "Hey Siri, tell Buddy to..."
  - Dictate text
  - POST to http://raspberrypi.local:5000/api/voice/command
  - Show confirmation

### Supported Commands (MVP):
```
"Add [item] to grocery list"
"Add [item] to other list"
"Add [item] to shopping list"  (defaults to grocery)
"Add TODO [task]"
```

### Success Criteria:
- ✓ Can use Siri to add grocery items
- ✓ Items appear in dashboard within seconds
- ✓ Shortcut provides success/error feedback
- ✓ Command parsing handles common variations

### Future Enhancements (post-MVP):
- More complex commands ("mark [todo] as complete")
- Natural language processing (NLP) for flexible phrasing
- Dedicated voice hardware (USB mic on Pi)

---

## Phase 6: Polish & Enhancement ✨
**Goal**: Improve UX and add nice-to-have features  
**Duration**: Ongoing

### Potential Features:
- [ ] Dark mode for dashboard
- [ ] Edit TODOs (not just add/delete)
- [ ] Recurring TODOs
- [ ] Email notifications for important events
- [ ] Weather widget
- [ ] Mark emails as read from dashboard
- [ ] Shopping list history/analytics
- [ ] Export shopping list to phone
- [ ] Multi-user support (family members)
- [ ] Custom wake word for voice commands
- [ ] Offline mode with cached data

### Performance Optimizations:
- [ ] Reduce API polling frequency (intelligent scheduling)
- [ ] Add database indexes
- [ ] Implement proper caching headers
- [ ] Optimize frontend bundle size

---

## Token-Saving Tips for Each Phase

### When Starting a Phase:
```markdown
<!-- Efficient prompt example -->
"I'm starting Phase 2 (Gmail Integration) from PHASES.md. 
I've completed Phase 1 - the basic dashboard works.
Gmail API research findings are in RESEARCH.md.
Please help me implement the OAuth2 flow."
```

### When Asking for Help:
- ✓ Reference specific files: "See ARCHITECTURE.md lines 45-60"
- ✓ Include error messages verbatim
- ✓ State what you've already tried
- ✗ Don't ask AI to re-read entire project

### After Completing a Phase:
```markdown
<!-- Update this file -->
## Phase 1: Minimal Local Dashboard ✅ COMPLETE

### Completed:
- Basic web server working
- SQLite database implemented
- All CRUD operations functional

### Deviations from Plan:
- Used FastAPI instead of Flask (better async support)

### Lessons Learned:
- SQLite locking issues on Pi - need WAL mode
- Alpine.js simpler than React for this use case

### Next Steps:
- Begin Phase 2 (Gmail Integration)
```

---

## Emergency Pivot Points

<!-- If research reveals blockers, pivot here -->

### If Gmail API Doesn't Work:
- **Alternative**: IMAP integration (less features, no OAuth2)
- **Alternative**: Manual email entry (defeats purpose)
- **Decision**: Drop email feature entirely?

### If Voice Commands Too Complex:
- **Alternative**: Skip voice, focus on web UI only
- **Alternative**: Use third-party service (Alexa skill)

### If Raspberry Pi Too Slow:
- **Alternative**: Run on old laptop or desktop instead
- **Alternative**: Optimize by dropping features

---

## Summary: Phase Gate Checklist

Before moving to next phase:
- [ ] Current phase fully functional
- [ ] All success criteria met
- [ ] Code committed/backed up
- [ ] PHASES.md updated with findings
- [ ] New unknowns documented in RESEARCH.md
- [ ] Architecture updated if design changed

**DO NOT SKIP PHASES - each builds on the previous!**
