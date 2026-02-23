# Decision Log

This document tracks major architectural and feature decisions, pivots, and course corrections.

---

## [2026-02-23] Pivot: Blog Section Instead of Gmail Integration

**Status**: Decided

**Context**:
- Originally planned Gmail integration for email monitoring
- Gmail OAuth implementation started but not completed
- Reconsidering the value and complexity of email integration, and possible security concerns (and honestly, may not even find it that useful)

**Decision**:
Replace Gmail integration with a Blog section for writing and publishing personal content.

**Reasoning**:
- Simpler to implement and maintain
- More aligned with personal dashboard use case
- Reduces external API dependencies
- Gmail integration requires ongoing OAuth maintenance
- Blog provides more creative/expressive outlet

**Consequences**:
- Remove/deprecate: `gmail_service.py`, Gmail-related routes in `app.py`, Gmail UI in `index.html`
- Add: blog planning strategy in `phases.
- Keep: Email cache table (can repurpose for blog post storage or remove)
- Update: Frontend to replace Gmail section with blog section

**Implementation**:
- [ ] Update PHASES.md to replace Gmail phase with Blog phase
- [ ] Archive gmail_service.py (move to archive/ folder)
- [ ] Add blog features to schema.sql
- [ ] Implement blog CRUD API
- [ ] Update frontend with blog UI

---

## Template for Future Decisions

**Status**: [Proposed | Decided | Deprecated | Superseded]

**Context**:
What problem are we trying to solve? What's the current situation?

**Decision**:
What are we doing? (Keep this concise)

**Reasoning**:
Why this approach? What alternatives were considered?

**Consequences**:
What changes as a result? What are the tradeoffs?

**Implementation**:
Key tasks or changes needed.
