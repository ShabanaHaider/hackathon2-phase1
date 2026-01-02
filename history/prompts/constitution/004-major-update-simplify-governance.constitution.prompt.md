---
id: 004
title: Major update simplify governance v2.0.0
stage: constitution
date: 2026-01-01
surface: agent
model: claude-sonnet-4-5-20250929
feature: none
branch: 001-advanced-features
user: user
command: /sp.constitution
labels: ["constitution", "major-update", "simplification", "governance", "agent-roles"]
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

# Todo CLI App Constitution - Updated

## 1. Purpose
This project demonstrates **spec-driven, agentic software development** using:
- Claude Code
- Spec-Kit Plus
- Python 3.13+
- UV
- Command Line Interface (CLI)

The goal is to build a **working in-memory Todo application** that supports advanced features with an improved, interactive user interface.

## 2. Scope

### In Scope:
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

### Out of Scope:
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

## 4. Agentic Dev Stack Workflow (Mandatory)

All work must follow this order:
1. Constitution (this document)
2. Specification → `/sp.specify`
3. Plan → `/sp.plan`
4. Tasks → `/sp.tasks`
5. Implementation → `/sp.implement`

## 5. Agent Roles

| Agent | Responsibility |
|-------|----------------|
| Orchestrator | Governs workflow enforcement, verifies specs and tasks |
| SpecificationAgent | Functional requirements |
| PlanningAgent | Architecture and flow |
| TaskAgent | Task decomposition |
| ImplementationAgent | Claude Code execution |
| InputValidationAgent | Input validation and error handling |

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
The project is complete when:
- All 10 features function correctly
- The CLI runs without errors
- Code matches the approved specifications
- Skills and workflow rules are enforced

## 10. Amendment Policy
This constitution may be amended if:
- A new specification explicitly requires it
- The change is documented and approved

## Response snapshot

Constitution successfully updated from v1.1.0 to v2.0.0 (MAJOR version bump).

**Version Bump Rationale**: MAJOR because:
- Backward incompatible: Removed RecurringTaskAgent and NotificationAgent from agent table
- Removed Section 11 (Governing Principle) entirely
- Removed several traceability and quality bar requirements
- Simplified governance structure significantly

**Key Changes**:

1. **Purpose** - Added mention of "improved, interactive user interface"

2. **Scope Features** - Regrouped and clarified:
   - Now explicitly labeled as "5 basic, 3 intermediate, 2 advanced"
   - Feature #7: "Categorize tasks" → "Categorize tasks (work/home)" (more specific)
   - Feature #8: "Set due dates" → "Set due dates (date/time picker and reminders)" (expanded)
   - Feature #10: Changed from "Due date reminders and notifications" to "Refined interactive CLI interface for task management" (NEW focus on UX)

3. **Agent Roles** - Simplified:
   - Removed RecurringTaskAgent
   - Removed NotificationAgent
   - Removed detailed Orchestrator subsection (kept in table only)
   - Now 6 agents instead of 7

4. **Skills Enforcement** - Simplified:
   - Reduced from detailed subsection with 4+ bullets to just 2 bullets
   - Removed "Orchestrator Responsibilities" subsection

5. **Traceability Rules** - Simplified:
   - Removed "❌ No manual coding"
   - Removed "✅ All iterations must be preserved"

6. **Quality Bar** - Simplified:
   - Removed "Development process is fully auditable"

7. **Governing Principle** - Removed:
   - Entire Section 11 removed (was: "This project prioritizes disciplined, traceable, agentic development...")

8. **Out of Scope** - Simplified:
   - Removed "Manual code edits" from out of scope list

**Files Modified**:
- .specify/memory/constitution.md

**Templates Requiring Review**:
- ⚠️ plan-template.md (agent role references may need update)
- ⚠️ tasks-template.md (agent role references may need update)

**Impact Assessment**:
- Existing specs/plans that reference RecurringTaskAgent or NotificationAgent will need reconciliation
- Simplified governance may affect enforcement rigor
- Removed "iterations must be preserved" may affect audit trail expectations

## Outcome

- ✅ Impact: Constitution simplified from 11 sections to 10; reduced from 7 agents to 6; streamlined governance
- 🧪 Tests: N/A (constitution document)
- 📁 Files: Modified .specify/memory/constitution.md with version 2.0.0
- 🔁 Next prompts: Review existing feature specs/plans for agent role references; consider impact on workflow enforcement
- 🧠 Reflection: Major simplification reduces complexity but may affect traceability and audit capabilities; feature #10 redefined from notifications to interactive UI (significant scope change)

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): Manual validation - PASS (version incremented correctly, all changes applied)
- Prompt variant (if applicable): Standard constitution update workflow
- Next experiment (smallest change to try): Monitor impact of removed agents and governance principles on development workflow
