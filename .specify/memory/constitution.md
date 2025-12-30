<!--
Sync Impact Report
==================
Version Change: None → 1.0.0 (Initial Ratification)
Status: Placeholder template replaced with human-authored constitution

Modified Principles: N/A (all new)
Added Sections:
  - Purpose
  - Scope (In Scope / Out of Scope)
  - Technology Stack (Fixed)
  - Agentic Dev Stack Workflow (Mandatory)
  - Agent Roles
  - Skills Registry
  - Skills Enforcement
  - Traceability Rules (Non-Negotiable)
  - Quality Bar
  - Amendment Policy
  - Governing Principle
Removed Sections: Template principles (replaced entirely)

Templates Status:
  ✅ .specify/memory/constitution.md - Updated (this file)
  ⚠ .specify/templates/plan-template.md - May need review for Constitution Check alignment
  ⚠ .specify/templates/spec-template.md - May need review for scope/requirements alignment
  ⚠ .specify/templates/tasks-template.md - May need review for task categorization
  ⚠ .claude/commands/*.md - May need review for references

Follow-up TODOs: None
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

The goal is to build a **working in-memory Todo application** while strictly enforcing the **Agentic Dev Stack workflow**.
Process correctness is as important as functional correctness.

## 2. Scope

### In Scope

- Console-based (CLI) Todo application
- Tasks stored entirely **in memory**
- Five basic features:
  1. Add task
  2. View tasks
  3. Update task
  4. Delete task
  5. Mark task complete / incomplete
- Development via Claude Code only
- Spec-Kit Plus artifacts for all phases

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

Agents may only act within their assigned roles.

## 6. Skills Registry

All agents must operate within the bounds of the approved skills defined in `.claude/skills.md`.

Skills define **what an agent is allowed to do**, not just what it can do.

## 7. Skills Enforcement

### Enforcement Rules

- Orchestrator MUST enforce all declared agent skills
- Agents MAY NOT act outside their defined skill scope
- Undeclared or implicit skills are prohibited
- Skill violations are treated as **spec violations**
- Any violation MUST halt execution and require correction

### Orchestrator Responsibilities

Orchestrator is explicitly responsible for:

- Verifying skill compliance before approving artifacts
- Blocking unauthorized actions by any agent
- Maintaining traceability between skills, specs, plans, tasks, and code
- Preventing scope creep and silent behavior changes

Skills enforcement applies globally unless explicitly overridden by an approved specification.

## 8. Traceability Rules (Non-Negotiable)

- ❌ No code without a **Task ID**
- ❌ No task without an **approved specification**
- ❌ No specification without this constitution
- ❌ No manual coding
- ✅ Every artifact must be traceable to a spec file
- ✅ All iterations must be preserved

Missing or undocumented files invalidate the workflow.

## 9. Quality Bar

The project is complete only when:

- All five required features function correctly
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

> **This project prioritizes disciplined, traceable, agentic development.
> Working code without process integrity is considered incomplete.**

---

**Version**: 1.0.0 | **Ratified**: 2025-12-30 | **Last Amended**: 2025-12-30
