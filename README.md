# Raspberry Pi Personal Dashboard

A locally-hosted dashboard for displaying daily essentials: emails, TODOs, shopping lists, and calendar events. Supports web UI and voice input.

---

## 🚧 Project Status: Planning Phase

This project is in **Phase 0 (Research & Planning)**. No code has been written yet.

**Current Work**: Answering critical feasibility questions before implementation.

---

## 📁 Project Structure

```
raspberry-pi-dashboard/
├── CLAUDE.md          # Context file for AI assistants (read this first!)
├── PROJECT.md         # Vision, features, and open questions
├── RESEARCH.md        # Unknowns requiring investigation
├── ARCHITECTURE.md    # Proposed system design
├── PHASES.md          # Development roadmap (phase-by-phase plan)
└── README.md          # This file
```

---

## 📖 For Contributors / Future Me

### Getting Started
1. **Read PROJECT.md** to understand the vision
2. **Check RESEARCH.md** to see what needs investigation
3. **Review PHASES.md** to know what phase we're in
4. **Read CLAUDE.md** when working with AI assistants

### Working with AI (Claude, Copilot, etc.)
To maximize token efficiency:
- Reference specific files instead of re-explaining the project
- Update documentation as you make progress
- See CLAUDE.md for detailed AI collaboration tips

### Current Phase: Phase 0
**Goal**: Complete all HIGH-priority research items in RESEARCH.md

**Next Steps**:
1. Research Gmail API capabilities and OAuth2 flow
2. Test Google Calendar API integration
3. Finalize technology stack (FastAPI vs. Flask, etc.)
4. Make architectural decisions based on research findings

Do not proceed to Phase 1 (coding) until research is complete!

---

## 🎯 End Goal

A Raspberry Pi that displays:
- Unread Gmail messages (last 20 days)
- Daily TODO list
- Shopping lists (groceries & other)
- Today's calendar events + upcoming events (3-5 days)

Input methods:
- Web UI (accessible via WiFi)
- Voice commands (e.g., "Hey Siri, tell Buddy to add milk to grocery list")

---

## 🔧 Future Setup Instructions

<!-- Will be filled in during Phase 4 (Raspberry Pi deployment) -->

Setup instructions will be added once we reach Phase 4.

For now, focus on research and planning.

---

## 📚 Documentation Philosophy

This project prioritizes **documentation over premature code**. Why?

1. **Token Efficiency**: Documented decisions prevent re-explaining to AI
2. **Risk Mitigation**: Research validates feasibility before wasting effort
3. **Incremental Progress**: Clear phases prevent half-finished features
4. **Future-Proofing**: Well-documented context helps future you (or others)

---

## ❓ Questions?

See PROJECT.md for the full vision and open questions.

See RESEARCH.md for what's currently being investigated.

---

**Last Updated**: February 19, 2026  
**Phase**: 0 (Research & Planning)  
**Status**: Active
