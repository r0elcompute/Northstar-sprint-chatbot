# Northstar Support Chatbot — Team Charter

## Team Information

**Team Name:** Titans

**Project:** Northstar Retail Co. Support Chatbot

**Team Members:**
- Constance Mukenyi — Frontend / UX, Team Lead
- Christine Wanja — AI/Automation
- Fanuel Rodgers — Backend
- Rachael Hinga — Database
- Didymus Kiai — Integration, QA/Documentation

**Project Repository:** https://github.com/r0elcompute/Northstar-sprint-chatbot

---

## 1. Team Purpose

Team Titans is building the Northstar Support Deflection MVP: a chatbot that lets Northstar Retail Co. customers get instant answers on two common ticket types — **Order Status** and **Returns/Refunds** — without waiting on a human agent. The goal is to demonstrate an end-to-end flow (customer message → intent detection → database lookup → AI-generated response) that deflects the most common, repetitive support tickets, freeing human agents for more complex issues.

---

## 2. Team Roles and Responsibilities

Constance Mukenyi — Frontend / UX, Team Lead: Customer-facing chat interface, UI states, coordinating the team and this charter.
Christine Wanja — AI/Automation: Intent detection, conversation flow, AI response generation.
Fanuel Rodgers — Backend: Django API, endpoints connecting frontend, AI, and database.
Rachael Hinga — Database: MySQL schema, Railway-hosted instance, seed/test data.
Didymus Kiai — Integration, QA/Documentation: End-to-end testing, cross-team integration, project documentation.
Each member owns their layer end-to-end (design, build, test) but is expected to coordinate at integration points — e.g. agreeing on request/response shapes before building against them.

---

## 3. Communication

- **Primary channel:** WhatsApp group. This is where day-to-day updates, questions, and blockers are posted.
- **Tagging:** Use @mentions when a message needs a specific person's attention, so it doesn't get lost in general chat.
- **Response time:** No strict SLA, but the team generally responds within the hour when active. If something is blocking your work and you haven't heard back, it's fine to follow up rather than wait indefinitely.
- **Progress updates:** When you finish a piece of work or hit a milestone, post a short update in the group so the rest of the team knows what's ready to integrate against.
- **Async-first:** Most coordination happens asynchronously in writing, so decisions and confirmations should be posted in the group, not just agreed verbally, so there's a record everyone can refer back to.
- **Scheduled calls:** Used occasionally, typically when a written back-and-forth would be slower than just talking it through. See Section 9.

---

## 4. GitHub Workflow

### Git & GitHub Workflow Rules

 1. **Branch Management**
   * Do not commit directly to `main`.
   * Create feature branches using the naming format: `feature/<feature-name>` or `fix/<bug-name>`.

 2. **Keeping Branches Updated**
   * Frequently pull/merge updates from `main` into your working branch to avoid large merge conflicts.
   * Test your code locally after pulling updates before creating a PR.

 3. **Pull Requests (PRs) & Code Reviews**
   * All code entering `main` requires a GitHub Pull Request.
   * Include a short summary of changes and local test results in the PR description.
   * Every PR must be reviewed and approved by at least one team member before merging.

 4. **Security & Secrets**
   * Never commit API keys, database credentials, or `.env` files. Ensure `.gitignore` is active.

---

## 5. Task Management

- Tasks are broken down by layer (frontend, AI/automation, backend, database, integration/QA) and owned individually, matching the roles in Section 2.
- Each member plans their own work in phases (foundation → implementation → integration/testing), as reflected in each member's individual work plan shared with the team.
- Deadlines are agreed as a team around key integration checkpoints — e.g. "backend endpoints ready," "seed data ready," "frontend can call live endpoints" — rather than rigid daily deadlines, since later phases depend on earlier ones finishing first.
- If a member is blocked because a dependency (another member's endpoint, schema, or data) isn't ready yet, they raise it in the WhatsApp group immediately rather than waiting silently.
- The team lead (Constance) tracks overall progress across roles and flags if any area is falling behind the others in a way that risks integration.

---

## 6. Definition of Done
The team should agree that a task is "Done" only when:

The agreed work has been completed.
The code/documentation has been committed to the member's branch.
The change has been reviewed by another teammate where applicable.
The PR has been approved and merged into main.
The relevant documentation has been updated.
The feature/task has been tested.
Any known issues are recorded.

## 7. Code Review and Pull Requests

- Every PR should have a clear title and a short description: what changed, why, and how it was tested locally.
- Reviewers check that the change matches what the PR description claims, doesn't break existing functionality, and follows the branch-naming and commit conventions in Section 4.
- Reviews focus on integration correctness first (does this match what other layers expect from it — e.g. response shapes, field names) and code quality second.
- If a reviewer requests changes, the PR author addresses them and re-requests review rather than merging over open feedback.
- At least one approval is required before merge, per Section 4. For changes affecting more than one person's layer (e.g. an API contract change), both affected members should review.
- Small, frequent PRs are preferred over large, infrequent ones — easier to review, easier to catch integration issues early.

---

## 8. Conflict Resolution

- Disagreements about technical approach are first discussed in the WhatsApp group; if it's not resolving quickly in writing, either party can call for a quick sync (see Section 9) instead of letting it drag out asynchronously.
- Technical disagreements are settled by what best serves the MVP scope and deadline — not by seniority or who raised it first. When it's a close call, the team lead makes the final decision so the team isn't blocked.
- Disagreements about workload or missed commitments are raised directly and respectfully with the person involved first, before escalating to the whole group.
- The team assumes good faith: most conflicts come from unclear requirements or crossed wires between layers, not from anyone acting in bad faith.
- Any conflict that can't be resolved between the people involved is brought to the team lead to help mediate.

---

## 9. Meetings and Progress Updates

- **Format:** Calls are scheduled as needed rather than on a fixed recurring basis — called when the team hits a decision point, blocker, or integration step that benefits from real-time discussion.
- **Purpose:** Meetings are for things that are slow over chat: resolving disagreements, planning integration work, or unblocking someone stuck on a dependency from another member.
- **Outside of calls:** Routine progress updates don't need a meeting — they go in the WhatsApp group as async status posts.
- **After a call:** Any decision made verbally should be summarized back in the WhatsApp group afterward, so members who weren't on the call stay in sync.

---

## 10. Accountability

- Each member is accountable for their own layer being ready by the integration checkpoints agreed in Section 5.
- Progress is visible through GitHub (commits, PRs, merged work) — see Section 11 — rather than relying on self-reported status alone.
- If a member is stuck or falling behind, they're expected to say so in the group early, not the day something is due — the team would rather help unblock someone than find out late.
- The team lead follows up directly with anyone who's gone quiet or missed an agreed checkpoint, before it affects other members' work.
- Missed commitments are addressed as a team conversation focused on solving the blocker, not blame — but repeated, unexplained non-delivery is escalated by the team lead as needed (e.g. to the course facilitator, if applicable).

---

## 11. Contribution Tracking

The team should track contributions through GitHub:

Each member works primarily from their own feature/task branch.
Each meaningful change should have a GitHub commit.
Larger changes should use a Pull Request.
PRs should identify what was changed and why.
Teammates review each other's PRs.
Issues/tasks are assigned to an owner.
The Project Board records status: Todo → In Progress → Review → Done.
Contributions should be visible through commits, PRs, reviews, and completed tasks.
Team members should not directly overwrite another person's work.

## 12. Team Agreement

By contributing to this repository, each team member agrees to:
- Follow the branching, PR, and review workflow in Sections 4 and 7.
- Communicate blockers and progress honestly and promptly, per Sections 3 and 10.
- Respect the scope of their assigned layer while staying available to help with integration issues that cross layers.
- Treat this charter as a living document — if something here stops matching how the team actually works, raise it and update it rather than quietly ignoring it.

---

## Sign-Off

- Constance Mukenyi — Frontend / UX, Team Lead
- Christine Wanja — AI/Automation
- Fanuel Rodgers — Backend
- Rachael Hinga — Database
- Didymus Kiai — Integration, QA/Documentation
