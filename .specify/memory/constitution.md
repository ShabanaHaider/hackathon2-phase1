<!--
Sync Impact Report
==================
Version Change: 1.1.0 → 2.0.0 (MAJOR)
Rationale: Backward incompatible changes - removed agents, simplified governance, redefined features

Modified Principles:
  - Purpose: Added "improved, interactive user interface"
  - Scope features: Regrouped as 5 basic, 3 intermediate, 2 advanced
  - Feature #7: "Categorize tasks" → "Categorize tasks (work/home)" (more specific)
  - Feature #8: "Set due dates" → "Set due dates (date/time picker and reminders)" (expanded description)
  - Feature #10: "Due date reminders and notifications" → "Refined interactive CLI interface" (NEW focus)

Removed Sections:
  - Section 5: Orchestrator detailed subsection (kept table only)
  - Section 7: Skills Enforcement detailed subsections (simplified to 2 bullets)
  - Section 8: "All iterations must be preserved" rule
  - Section 9: "Development process is fully auditable" quality bar item
  - Section 11: Governing Principle (entire section removed)
  - Agent Roles: RecurringTaskAgent and NotificationAgent removed from table
  - Out of Scope: "Manual code edits" removed

Simplified Sections:
  - Agent Roles: Now single table without Orchestrator subsection
  - Skills Enforcement: Reduced from 4+ bullets to 2 bullets
  - Out of Scope: Reduced from 5 items to 4 items
  - Quality Bar: Reduced from 5 items to 4 items

Templates Status:
  ✅ .specify/memory/constitution.md - Updated (this file)
  ⚠️ .specify/templates/plan-template.md - Review needed (agent roles changed)
  ⚠️ .specify/templates/tasks-template.md - Review needed (agent roles changed)
  ✅ .specify/templates/spec-template.md - No changes needed
  ℹ️ .specify/templates/commands/ - No command files present

Follow-up TODOs:
  - Review plan-template.md for agent role references
  - Review tasks-template.md for agent role references
  - Consider impact on existing specs/plans that reference removed agents
-->

# Todo CLI App Constitution
**Phase I – In-Memory CLI Todo Application**

## 1. Purpose

This project exists to demonstrate **spec-driven, agentic software development** using:

- Claude Code
- Spec-Kit Plus
- Python 3.13+
- UV
- Command Line Interface (CLI)

The goal is to build a **working in-memory Todo application** that supports advanced features with an improved, interactive user interface.

## 2. Scope

### In Scope

- Console-based (CLI) Todo application
- Tasks stored entirely **in memory**
- **10 core features** (5 basic, 3 intermediate, 2 advanced):
  1. Add task
  2. View tasks
  3. Update task
  4. Delete task
  5. Mark task complete/incomplete
  6. Assign priority (high/medium/low)
  7. Categorize tasks (work/home)
  8. Set due dates (date/time picker and reminders)
  9. Recurring tasks (daily, weekly, etc.)
  10. Refined interactive CLI interface for task management

### Out of Scope

- File or database persistence
- GUI (graphical user interface)
- Authentication or multi-user support
- Background services or APIs

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

| Agent | Responsibility |
|-------|----------------|
| Orchestrator | Governs workflow enforcement, verifies specs and tasks |
| SpecificationAgent | Functional requirements |
| PlanningAgent | Architecture and flow |
| TaskAgent | Task decomposition |
| ImplementationAgent | Claude Code execution |
| InputValidationAgent | Input validation and error handling |

Agents may only act within their assigned roles.

## 6. Skills Registry

All agents must operate within the bounds of the approved skills defined in `.claude/skills.md`.

## 7. Skills Enforcement

- Orchestrator MUST enforce all declared agent skills
- Agents MAY NOT act outside their defined skill scope

## 8. Traceability Rules

- ❌ No code without a **Task ID**
- ❌ No task without an **approved specification**
- ❌ No specification without this constitution
- ✅ Every artifact must be traceable to a spec file

## 9. Quality Bar

The project is complete only when:

- All 10 features function correctly
- The CLI application runs without errors
- Code matches the approved specifications
- Skills and workflow rules are enforced

## 10. Amendment Policy

This constitution may only be amended if:

- A new specification explicitly requires it
- The change is documented and approved

Silent or retroactive changes are prohibited.

---

**Version**: 2.0.0 | **Ratified**: 2025-12-30 | **Last Amended**: 2026-01-01
