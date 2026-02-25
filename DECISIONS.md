# Decision Log

This document tracks major architectural and feature decisions, pivots, and course corrections.

---

## [2026-02-24] Pivot: Next.js Instead of Flask

**Status**: Decided

**Context**:
- Current implementation uses Flask (Python) backend with vanilla JavaScript frontend
- Blog scaffolding just completed in Flask
- Want to explore modern full-stack framework for comparison

**Decision**:
Rewrite application using Next.js (React + TypeScript) with API routes.

**Reasoning**:
- Modern development experience with React components
- Built-in TypeScript support
- API routes eliminate need for separate backend
- Better performance with SSR/SSG capabilities
- More familiar for frontend-focused development
- Easier deployment options (Vercel, etc.)
- PostgreSQL can still be used as database

**Consequences**:
- Keep Flask code in `/flask-version` for reference
- New Next.js app structure in project root or separate directory
- Reimplement: Blog, Todos, Groceries in React components
- Database layer: Use Prisma or pg directly from Next.js API routes
- Deployment: Can use Vercel, or self-host with Node.js

**Implementation**:
- [ ] Set up Next.js project structure
- [ ] Configure PostgreSQL connection in Next.js
- [ ] Create API routes for blog, todos, groceries
- [ ] Build React UI components
- [ ] Keep Flask version for architecture comparison

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
