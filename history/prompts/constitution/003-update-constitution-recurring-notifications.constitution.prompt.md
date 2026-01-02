---
id: 003
title: Update constitution v1.1.0 add features
stage: constitution
date: 2026-01-01
surface: agent
model: claude-sonnet-4-5-20250929
feature: none
branch: main
user: user
command: /sp.constitution
labels: ["constitution", "features", "agents", "recurring-tasks", "notifications"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
 - .specify/memory/constitution.md
tests:
 - none
---

## Prompt

# Todo CLI App Constitution
**Phase I – In-Memory CLI Todo Application**

## 1. Purpose

This project exists to demonstrate **spec-driven, agentic software development** using:

- Claude Code
- Spec-Kit Plus
- Python 3.13+
- UV
- Command Line Interface (CLI)

The goal is to build a **working in-memory Todo application** while strictly enforcing the **Agentic Dev Stack workflow**.
Process correctness is as important as functional correctness.

## 2. Scope

### In Scope

- Console-based (CLI) Todo application
- Tasks stored entirely **in memory**
- Ten core features:
  1. Add task
  2. View tasks
  3. Update task
  4. Delete task
  5. Mark task complete / incomplete
  6. Assign priority (high/medium/low)
  7. Categorize tasks
  8. Set due dates
  9. Recurring tasks (auto-reschedule tasks like "weekly meeting")
  10. Due date reminders and time notifications (browser notifications)

### Out of Scope

- File or database persistence
- GUI or web interfaces
- Authentication or multi-user support
- Background services or APIs
- Manual code edits

## 3. Technology Stack (Fixed)

- Python **3.13+**
- **UV** for environment and execution
- **Claude Code** for implementation
- **Spec-Kit Plus** for specifications
- **CLI-only** interaction

Any deviation requires an approved specification update.

## 4. Agentic Dev Stack Workflow (Mandatory)

All work must follow this order:

1. Constitution (this document)
2. Specification → `/sp.specify`
3. Plan → `/sp.plan`
4. Tasks → `/sp.tasks`
5. Implementation → `/sp.implement`

### Enforcement

- No phase may begin before the previous phase is approved
- Orchestrator must block execution on any violation

## 5. Agent Roles

### Orchestrator

- Governs workflow enforcement
- Verifies constitution existence
- Approves or rejects specs, plans, and tasks
- Authorizes implementation
- Halts execution on violations

### Sub-Agents

| Agent | Responsibility |
|-------|----------------|
| SpecificationAgent | Functional requirements |
| PlanningAgent | Architecture and flow |
| TaskAgent | Task decomposition |
| ImplementationAgent | Claude Code execution |
| InputValidationAgent | Input validation and error handling |
| RecurringTaskAgent | Handle recurring tasks (e.g., "weekly meeting") |
| NotificationAgent | Responsible for handling due date notifications |

Agents may only act within their assigned roles.

## 6. Skills Registry

All agents must operate within the bounds of the approved skills defined in `.claude/skills.md`.

## 7. Skills Enforcement

Skills enforcement applies globally unless explicitly overridden by an approved specification.

## 8. Traceability Rules

- ❌ No code without a **Task ID**
- ❌ No task without an **approved specification**
- ❌ No specification without this constitution
- ❌ No manual coding
- ✅ Every artifact must be traceable to a spec file
- ✅ All iterations must be preserved

## 9. Quality Bar

The project is complete only when:

- All ten required features function correctly
- The CLI application runs without errors
- Code matches the approved specifications
- Skills and workflow rules were enforced
- The development process is fully auditable

## 10. Amendment Policy

This constitution may only be amended if:

- A new specification explicitly requires it
- The change is documented and approved
- Traceability is preserved

Silent or retroactive changes are prohibited.

## 11. Governing Principle

> **This project prioritizes disciplined, traceable, agentic development.**
> **Working code without process integrity is considered incomplete.**

---

**Version**: 1.0.1 | **Ratified**: 2025-12-30 | **Last Amended**: 2026-01-01

## Response snapshot

Constitution successfully updated from v1.0.1 to v1.1.0 (MINOR version bump).

**Key Changes:**
- Added 2 new features: recurring tasks (#9) and due date reminders/notifications (#10)
- Added 2 new agents: RecurringTaskAgent and NotificationAgent
- Updated Quality Bar to reflect 10 features (was 8)
- Updated Sync Impact Report in constitution file header

**Files Modified:**
- .specify/memory/constitution.md

**Templates Validated:**
- plan-template.md: No changes needed (constitution check section exists)
- spec-template.md: No changes needed (already flexible)
- tasks-template.md: No changes needed (already flexible)
- commands/: No command files present

**Version Bump Rationale:**
MINOR bump appropriate because:
- New features added (recurring tasks, notifications)
- New agent roles introduced
- Backward compatible (existing 8 features still valid)
- No breaking changes to governance structure

## Outcome

- ✅ Impact: Constitution expanded from 8 to 10 features; added RecurringTaskAgent and NotificationAgent
- 🧪 Tests: N/A (constitution document)
- 📁 Files: Modified .specify/memory/constitution.md with version 1.1.0
- 🔁 Next prompts: Ready for /sp.specify to create specifications for new features (recurring tasks, notifications)
- 🧠 Reflection: Version incremented appropriately using semantic versioning; sync impact report documents all changes; templates remain compatible

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): Manual validation - PASS (all placeholders filled, version coherent, templates validated)
- Prompt variant (if applicable): Standard constitution update workflow
- Next experiment (smallest change to try): None required
