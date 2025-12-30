# Skills Documentation: Todo CLI App Phase 1

**Project**: Todo CLI Application (In-Memory Task Storage)
**Phase**: Phase I - Spec-Driven Development
**Last Updated**: 2025-12-30

This document defines all skills available for the Todo CLI App project. Each skill is owned by a specific agent and follows the Spec-Driven Development (SDD) methodology.

---

## Table of Contents

1. [Orchestrator Skills](#orchestrator-skills)
2. [Functional Spec Author Skills](#functional-spec-author-skills)
3. [Planning Agent Skills](#planning-agent-skills)
4. [Task Decomposer Skills](#task-decomposer-skills)
5. [Implementation Agent Skills](#implementation-agent-skills)

---

## Orchestrator Skills

**Owner**: `orchestrator` agent

The Orchestrator is the primary coordination agent for Phase I projects. It enforces the SDD workflow, validates prerequisites, and delegates to sub-agents. It never writes implementation code.

---

### Skill: Enforce SDD Workflow

**Purpose**: Guard the development process by blocking progress when prerequisites are missing or the workflow is violated.

**When to use**:
- At the start of any development request
- When verifying project readiness
- Before delegating to any sub-agent

**Inputs**:
- Current project phase (constitution, spec, plan, tasks, implementation)
- Available artifacts (file existence checks)
- User request type

**Step-by-Step process**:

1. **Identify the requested phase** from the user input or context
2. **Verify prerequisite artifacts exist**:
   - Constitution phase: No prerequisites
   - Specification phase: Constitution must exist at `.specify/memory/constitution.md`
   - Planning phase: Specification must exist at `specs/<feature>/spec.md`
   - Tasks phase: Plan must exist at `specs/<feature>/plan.md`
   - Implementation phase: Tasks must exist at `specs/<feature>/tasks.md`
3. **Check artifact approval status** if approval workflow is enabled
4. **Block and report** if prerequisites are missing:
   - State what is required
   - Identify which command to run
   - Do not proceed with implementation
5. **Delegate to appropriate sub-agent** when all prerequisites are met

**Output**:
- Delegation to sub-agent, OR
- Blocked message with required artifacts and next steps

**Failure Handling**:
- If prerequisite check fails: Block and display clear requirements
- If artifact exists but is malformed: Report specific issue
- If approval status is unclear: Request human clarification

---

### Skill: Coordinate Sub-Agents

**Purpose**: Route requests to the correct sub-agent with appropriate context and instructions.

**When to use**:
- After workflow enforcement passes
- When user requests a phase transition
- When delegating planning, specification, or task creation

**Inputs**:
- Target phase (spec, plan, tasks, implement)
- Feature context (feature name, branch)
- User request details

**Step-by-Step process**:

1. **Determine target agent** based on phase:
   - Specification → `functional-spec-author`
   - Planning → `planning-agent`
   - Tasks → `task-decomposer`
   - Implementation → `implementation-agent`
2. **Prepare delegation context**:
   - Feature name and branch
   - Available artifacts paths
   - Relevant user requirements
3. **Create delegation prompt**:
   - Clear objective
   - Required inputs
   - Success criteria
4. **Invoke the sub-agent** via handoff
5. **Review produced artifacts** for correctness
6. **Approve or request corrections** based on quality standards

**Output**:
- Delegated task to sub-agent
- Artifact review status (approved/rejected)
- Feedback for corrections if needed

**Failure Handling**:
- If sub-agent fails to produce valid artifact: Request retry with specific feedback
- If artifact violates constitution: Reject and explain violation
- If scope creep detected: Block and request clarification

---

### Skill: Validate Prerequisites

**Purpose**: Verify all required artifacts exist and are properly formed before proceeding to the next phase.

**When to use**:
- Before `/sp.specify` (check constitution)
- Before `/sp.plan` (check spec)
- Before `/sp.tasks` (check plan)
- Before `/sp.implement` (check tasks)

**Inputs**:
- Target phase
- Required artifact paths

**Step-by-Step process**:

1. **Identify required artifacts** for the target phase
2. **Check file existence** at each expected path
3. **Validate file contents**:
   - Not empty
   - Contains expected sections
   - Passes format validation
4. **Check approval status** if applicable
5. **Report validation results**:
   - All present: Proceed
   - Missing: List required files
   - Invalid: Specific issues found

**Output**:
- Validation status (PASS/FAIL)
- List of missing or invalid artifacts
- Recommended next steps

**Failure Handling**:
- Missing artifact: Block and identify required file
- Invalid artifact: Report specific validation error
- Empty or corrupted file: Request regeneration

---

## Functional Spec Author Skills

**Owner**: `functional-spec-author` agent

The Functional Spec Author creates detailed, testable specifications for features. It writes only specifications—no code, no implementation details, no task breakdowns.

---

### Skill: Write Feature Specification

**Purpose**: Create a comprehensive functional specification document from a natural language feature description.

**When to use**:
- When `/sp.specify` is invoked
- When a new feature needs documentation before implementation
- When existing spec requires updates or clarifications

**Inputs**:
- Feature description (user input after `/sp.specify`)
- Feature short name (derived from description)
- Feature number (auto-incremented from existing branches)
- Constitution principles (from `.specify/memory/constitution.md`)

**Step-by-Step process**:

1. **Parse feature description**:
   - Extract actors, actions, data, constraints
   - Identify the 5 core Todo App features being addressed
2. **Generate feature short name** (2-4 words, action-noun format)
3. **Check for existing branches** and determine next feature number
4. **Run setup script** to create branch and initialize spec file
5. **Load specification template** from `.specify/templates/spec-template.md`
6. **Fill specification sections**:
   - Feature Overview: Description, value proposition, success criteria
   - User Stories: As a [role], I want [goal], so that [benefit]
   - Functional Requirements: Numbered, testable requirements with pass/fail criteria
   - CLI Interface: Exact syntax, arguments, options, expected outputs
   - Data Model: Task entity properties, constraints, valid states
   - Acceptance Criteria: Given-When-Then format for each requirement
   - Error Handling: All error conditions with user-facing messages
7. **Document assumptions** for any unspecified details
8. **Limit clarifications** to maximum 3 critical items
9. **Write spec to file** at `specs/<feature>/spec.md`

**Output**:
- Feature branch created and checked out
- Specification document at `specs/<feature>/spec.md`
- Quality checklist at `specs/<feature>/checklists/requirements.md`
- Summary of readiness for next phase

**Failure Handling**:
- Empty feature description: Error "No feature description provided"
- Unclear user scenarios: Error "Cannot determine user scenarios"
- More than 3 clarifications needed: Keep only top 3, make informed guesses for rest
- Validation failures: Iterate up to 3 times, then warn user

---

### Skill: Validate Specification Quality

**Purpose**: Ensure specifications meet quality standards before proceeding to planning.

**When to use**:
- After writing initial specification
- Before declaring spec ready for `/sp.plan`
- During specification review

**Inputs**:
- Specification file path
- Quality checklist template

**Step-by-Step process**:

1. **Generate quality checklist** at `FEATURE_DIR/checklists/requirements.md`
2. **Validate each criterion**:
   - Content Quality: No implementation details, user-focused, all sections complete
   - Requirement Completeness: Testable, measurable success criteria, edge cases identified
   - Feature Readiness: Acceptance scenarios defined, requirements traceable
3. **Check for [NEEDS CLARIFICATION] markers**:
   - Count total markers
   - If more than 3: Keep only 3 most critical, make informed guesses for rest
4. **Present clarification questions** to user if markers remain:
   - Context: Relevant spec section
   - Options: At least 3 choices with implications
   - Wait for user response
5. **Update spec** with user clarifications
6. **Re-run validation** until all items pass
7. **Update checklist status** with results

**Output**:
- Completed quality checklist
- List of clarification questions (if any)
- Validation status (PASS/FAIL with issues)

**Failure Handling**:
- Validation fails after 3 iterations: Document remaining issues, warn user
- User clarification ambiguous: Ask follow-up for clarity
- Checklist file creation fails: Use agent-native tools as fallback

---

### Skill: Clarify Requirements

**Purpose**: Present clarification questions to users and update specification with resolved answers.

**When to use**:
- When specification contains [NEEDS CLARIFICATION] markers
- When requirements are ambiguous and impact scope or UX
- Before planning phase when clarifications remain

**Inputs**:
- Specification file with [NEEDS CLARIFICATION] markers
- List of clarification topics (max 3)

**Step-by-Step process**:

1. **Extract all [NEEDS CLARIFICATION] markers** from spec
2. **Prioritize by impact**: Scope > Security/Privacy > User Experience > Technical
3. **Limit to 3 most critical** if more exist
4. **Present questions to user** in markdown table format:
   - Question number and topic
   - Context (quoted spec section)
   - Specific question
   - Suggested answers with implications
5. **Wait for user response** with choices (e.g., "Q1: A, Q2: C, Q3: B")
6. **Update specification** by replacing each marker with user's answer
7. **Re-run validation** to ensure quality standards still met
8. **Confirm spec readiness** for planning phase

**Output**:
- Updated specification with no [NEEDS CLARIFICATION] markers
- List of resolved clarifications
- Validation confirmation

**Failure Handling**:
- User provides unclear choice: Ask for clarification
- User wants to defer decision: Mark with default, note in spec
- User provides custom answer: Verify it fits the context, then apply

---

## Planning Agent Skills

**Owner**: `planning-agent` agent

The Planning Agent creates architectural plans based on approved specifications. It produces documentation only—data models, contracts, research findings—no implementation code.

---

### Skill: Create Architectural Plan

**Purpose**: Generate a comprehensive architectural plan document from an approved specification.

**When to use**:
- When `/sp.plan` is invoked
- After specification is approved and ready for technical design
- When plan.md needs updates or refinements

**Inputs**:
- Specification file at `specs/<feature>/spec.md`
- Constitution at `.specify/memory/constitution.md`
- Plan template at `.specify/templates/plan-template.md`

**Step-by-Step process**:

1. **Run setup script** to identify feature directory and load context
2. **Read specification thoroughly**:
   - Extract 5 core features (add, view, update, delete, mark complete/incomplete)
   - Identify CLI interface requirements
   - Map data model requirements
3. **Read constitution principles** for constraints and guidelines
4. **Create plan.md sections**:
   - High-Level Architecture: CLI-only application structure, command routing
   - Module Breakdown: Command handlers, task storage, CLI interface layers
   - Data Flow: Command parsing → validation → storage → output
   - CLI Interaction Flow: Entry points, argument parsing, error handling
   - Key Design Decisions: Technology choices, data structure decisions
5. **Mark significant decisions** requiring ADR documentation with **[ADR NEEDED]**
6. **Validate against constitution**:
   - Ensure smallest viable change principle
   - Verify in-memory storage requirement
   - Confirm CLI-only interface
7. **Write plan to file** at `specs/<feature>/plan.md`

**Output**:
- Architectural plan document at `specs/<feature>/plan.md`
- List of design decisions needing ADR documentation
- Constitution compliance status

**Failure Handling**:
- Specification missing: Error and request `/sp.specify` first
- Specification incomplete: Request clarification before planning
- Constitution violation: Flag and explain, suggest compliant alternative
- Ambiguous requirements: Create [NEEDS CLARIFICATION] markers, limit to 3

---

### Skill: Generate Data Model

**Purpose**: Create a data model document defining entities, relationships, and constraints for the Todo CLI App.

**When to use**:
- During Phase 1 of planning
- When data entities need explicit definition
- As input for task generation

**Inputs**:
- Specification file with data requirements
- Feature context and requirements
- Plan template structure

**Step-by-Step process**:

1. **Extract entities from specification**:
   - Task entity: id, title, description, status, created_at, updated_at
   - Any supporting entities (if applicable for Phase 2+)
2. **Define entity properties**:
   - Property name and type
   - Validation rules
   - Required vs optional
   - Default values
3. **Define state transitions**:
   - Task status flow: incomplete → complete (and back if toggle supported)
4. **Document constraints**:
   - In-memory storage limitations
   - ID generation strategy
   - Title/description limits
5. **Map to user stories**:
   - Which entities each feature requires
   - Which properties each feature uses
6. **Write data-model.md** at `specs/<feature>/data-model.md`

**Output**:
- Data model document with entities, properties, relationships
- State transition diagrams (ASCII)
- Constraint specifications
- Feature-to-entity mapping

**Failure Handling**:
- Specification doesn't define data: Make reasonable assumptions, document them
- Conflicting requirements: Flag for clarification, suggest resolution
- Invalid property definitions: Correct and note the fix

---

### Skill: Create API Contracts

**Purpose**: Define CLI command contracts including syntax, arguments, outputs, and error conditions.

**When to use**:
- During Phase 1 of planning
- When CLI interface needs formal definition
- As input for implementation tasks

**Inputs**:
- Specification with CLI requirements
- Data model definitions
- Error handling requirements

**Step-by-Step process**:

1. **Identify all CLI commands** from specification:
   - `todo add --title TEXT --description TEXT`
   - `todo list`
   - `todo update ID [--title TEXT] [--description TEXT]`
   - `todo delete ID`
   - `todo complete ID`
   - `todo incomplete ID`
2. **Define each command contract**:
   - Exact syntax
   - Required arguments
   - Optional arguments
   - Default values
   - Expected output format (human-readable table/list)
   - Error conditions and messages
3. **Create contract files** in `specs/<feature>/contracts/`:
   - One file per command or consolidated YAML/JSON
   - Include examples for success and failure
4. **Validate contracts** against specification requirements
5. **Document edge cases**:
   - Empty task list for `list`
   - Invalid ID for update/delete/complete
   - Duplicate titles (if uniqueness required)

**Output**:
- Contract files at `specs/<feature>/contracts/`
- Command syntax documentation
- Error catalog with messages
- Usage examples

**Failure Handling**:
- Missing command in spec: Request clarification
- Ambiguous syntax: Choose sensible default, document assumption
- Conflicting outputs: Flag inconsistency, suggest resolution

---

### Skill: Conduct Technical Research

**Purpose**: Research technical decisions and document findings for later implementation.

**When to use**:
- During Phase 0 of planning
- When specification contains technical unknowns
- When best practices need verification

**Inputs**:
- List of [NEEDS CLARIFICATION] markers from plan
- Technology stack references (Python 3.13+, UV package manager)
- Integration requirements

**Step-by-Step process**:

1. **Identify research topics** from plan unknowns
2. **Research each topic**:
   - Best practices for Python CLI with click/argparse
   - In-memory data structure patterns
   - UV package configuration
3. **Document findings** in `research.md`:
   - Decision: What was chosen
   - Rationale: Why chosen
   - Alternatives considered: What else was evaluated
4. **Resolve [NEEDS CLARIFICATION] markers** with research findings
5. **Flag significant decisions** for ADR documentation

**Output**:
- Research document at `specs/<feature>/research.md`
- Resolved technical decisions
- Recommendations for implementation

**Failure Handling**:
- Unable to find information: Note gap, suggest human research
- Conflicting recommendations: Present options, let user decide
- Research topic out of scope: Defer to implementation agent

---

## Task Decomposer Skills

**Owner**: `task-decomposer` agent

The Task Decomposer transforms approved plans into executable, traceable task lists. It produces tasks.md only—no implementation code.

---

### Skill: Generate Task List

**Purpose**: Create a comprehensive, dependency-ordered task list from approved design artifacts.

**When to use**:
- When `/sp.tasks` is invoked
- After plan is approved
- When task list needs regeneration

**Inputs**:
- Plan document at `specs/<feature>/plan.md`
- Specification at `specs/<feature>/spec.md`
- Data model at `specs/<feature>/data-model.md` (if exists)
- Contracts at `specs/<feature>/contracts/` (if exists)
- Research at `specs/<feature>/research.md` (if exists)

**Step-by-Step process**:

1. **Run prerequisites check script** to identify available documents
2. **Read all available design documents**:
   - plan.md: Tech stack, architecture, file structure
   - spec.md: User stories with priorities (P1, P2, P3)
   - data-model.md: Entities and relationships
   - contracts/: API/CLI specifications
   - research.md: Technical decisions
3. **Organize tasks by phase**:
   - Phase 1: Setup (project initialization, dependency configuration)
   - Phase 2: Foundational (prerequisites for all user stories)
   - Phase 3+: User stories in priority order
   - Final Phase: Polish and cross-cutting concerns
4. **Generate each task with**:
   - Sequential ID (T001, T002, ...)
   - Clear action description with file path
   - Story label [US1], [US2], etc. for user story tasks
   - Parallel marker [P] if task can run concurrently
   - Dependencies (task numbers)
5. **Map tasks to specification**:
   - Each task traces to a requirement
   - All 5 features covered
6. **Write tasks.md** using template structure
7. **Report summary**:
   - Total task count
   - Tasks per user story
   - Parallel execution opportunities

**Output**:
- Tasks document at `specs/<feature>/tasks.md`
- Task count summary
- Dependency graph overview

**Failure Handling**:
- Missing required documents: Request `/sp.plan` first
- User story not fully covered: Flag gap, suggest task
- Circular dependencies detected: Request human resolution
- Task too large: Split into smaller atomic tasks

---

### Skill: Validate Task Completeness

**Purpose**: Verify that all specification requirements are covered by tasks and each task is independently testable.

**When to use**:
- After generating task list
- Before implementation phase
- During quality review

**Inputs**:
- Specification file
- Generated tasks file
- Data model and contracts (if available)

**Step-by-Step process**:

1. **Cross-reference specification requirements** with tasks:
   - Each functional requirement has at least one task
   - Each CLI command has implementation task
   - Error handling is covered
2. **Verify task independence**:
   - Each task can be completed alone
   - Dependencies are explicit
   - Parallel tasks don't share files
3. **Check acceptance criteria**:
   - Each task has clear done state
   - Tests are identified (if required)
   - Integration points documented
4. **Validate traceability**:
   - Task maps to specific spec section
   - No orphaned tasks without source
5. **Report coverage gaps** if found
6. **Update tasks.md** with validation results

**Output**:
- Coverage report (requirements mapped to tasks)
- Gap analysis
- Validation status (PASS/FAIL)

**Failure Handling**:
- Uncovered requirement: Add missing task
- Non-independent task: Refactor into atomic units
- Missing acceptance criteria: Add clear completion definition

---

### Skill: Organize Tasks by User Story

**Purpose**: Structure tasks so each user story can be implemented and tested independently.

**When to use**:
- During task generation
- When enabling incremental delivery
- When defining MVP scope

**Inputs**:
- Specification with user stories (P1, P2, P3...)
- Data model and contracts
- Priority ordering from specification

**Step-by-Step process**:

1. **Extract user stories** from specification with priorities
2. **Group tasks by user story**:
   - Tasks only for [US1] → US1 phase
   - Tasks shared by multiple stories → Foundational phase
   - Cross-cutting tasks → Final Polish phase
3. **Define independent test criteria** for each story:
   - What must work to consider story complete
   - How to verify without other stories
4. **Identify parallel execution opportunities**:
   - Tasks in different stories with no dependencies
   - Tasks affecting different files
5. **Suggest MVP scope** (typically User Story 1 only)
6. **Document story completion order** and dependencies

**Output**:
- Phase-organized task structure
- Independent test criteria per story
- Parallel execution examples
- MVP scope recommendation

**Failure Handling**:
- Story has blocking dependency: Document and suggest order
- Shared task affects multiple stories: Move to foundational
- Test criteria ambiguous: Define based on acceptance criteria

---

## Implementation Agent Skills

**Owner**: `implementation-agent` agent

The Implementation Agent is the only agent that writes implementation code. It executes approved tasks following the task list, respecting dependencies and quality standards.

---

### Skill: Execute Task

**Purpose**: Implement a single approved task from tasks.md following specification and plan.

**When to use**:
- When `/sp.implement` runs a task
- When implementing specific task (e.g., "Implement TASK-001")
- During sequential task execution

**Inputs**:
- Task ID and description from tasks.md
- Task phase and dependencies
- Specification references
- Plan architecture and data model
- File paths for creation/modification

**Step-by-Step process**:

1. **Confirm task scope**:
   - Read task ID, description, acceptance criteria
   - Identify files to create or modify
   - Check dependencies are completed
2. **Read related context**:
   - Plan.md for architecture guidance
   - Data model for entity definitions
   - Contracts for interface requirements
3. **Execute implementation**:
   - Create or modify files using Claude Code tools only
   - Follow PEP 8 and Python 3.13+ best practices
   - Use type hints for all function signatures
   - Write docstrings for public APIs
   - Implement CLI commands with click or argparse
   - Use in-memory data structures for task storage
4. **Test incrementally** if applicable
5. **Reference task ID** in all file changes and git commits
6. **Mark task complete** by updating tasks.md checkbox
7. **Report completion** with files created/modified

**Output**:
- Files created or modified
- Task marked complete in tasks.md
- Summary of implementation

**Failure Handling**:
- Ambiguous task: Stop, report blocker, await Orchestrator guidance
- Missing dependencies: Wait for dependency completion
- Conflict with previous task: Report to Orchestrator
- Implementation exceeds scope: Flag for review, do not proceed

---

### Skill: Validate Implementation

**Purpose**: Verify that completed implementation matches specification and passes quality checks.

**When to use**:
- After task implementation
- Before marking task complete
- During implementation phase checkpoints

**Inputs**:
- Task acceptance criteria
- Specification requirements
- Plan architecture
- Code quality standards from constitution

**Step-by-Step process**:

1. **Check acceptance criteria**:
   - Each criterion verified as complete
   - No incomplete items remaining
2. **Run quality checks**:
   - Code compiles/runs without errors
   - Type hints are correct and complete
   - No unrelated code changes
   - Task ID referenced in relevant actions
3. **Run tests** if applicable:
   - Unit tests pass
   - Integration tests pass (if task involves multiple components)
4. **Verify specification compliance**:
   - Implementation matches approved spec exactly
   - No scope creep
5. **Document any deviations**:
   - Note deviations from spec
   - Justify if deviation improves outcome
6. **Report validation status** to Orchestrator

**Output**:
- Validation status (PASS/FAIL)
- List of passing acceptance criteria
- Any deviations or issues found
- Recommendations if failing

**Failure Handling**:
- Acceptance criterion fails: Fix implementation or flag for clarification
- Quality check fails: Correct issue, re-validate
- Test fails: Debug and fix, or request clarification
- Scope creep detected: Revert changes, stick to approved task

---

### Skill: Report Progress

**Purpose**: Provide clear, traceable progress reports during implementation phase.

**When to use**:
- After completing each task
- At phase boundaries
- When blocked or requiring clarification
- At implementation completion

**Inputs**:
- Current task ID and status
- Completed tasks list
- Remaining tasks
- Blockers or issues

**Step-by-Step process**:

1. **Gather task status**:
   - Current task completion result
   - Files created and modified
   - Any deviations from plan
2. **Format report**:
   ```
   ✅ TASK-XXX COMPLETED

   Files Created:
   - path/to/file1.py
   - path/to/file2.py

   Files Modified:
   - path/to/file3.py

   Summary:
   - Brief description of implementation
   - Key decisions made
   - Any follow-ups needed
   ```
3. **Report blockers** if any:
   ```
   ⚠️ TASK-XXX BLOCKED

   Blocker Description:
   - Clear explanation of the obstacle

   Required Input:
   - Specific guidance needed from Orchestrator
   ```
4. **Update progress tracking** if project uses it
5. **Signal completion** to Orchestrator for approval

**Output**:
- Task completion or blocker report
- File inventory
- Summary of work done
- Next steps recommendation

**Failure Handling**:
- Unable to format report: Provide minimal status update
- Blocked without clear reason: Document partial progress, request guidance
- Task partially complete: Report what was done, what remains

---

### Skill: Execute Implementation Phase

**Purpose**: Orchestrate complete implementation phase by executing all tasks in dependency order.

**When to use**:
- When `/sp.implement` is invoked
- When user requests full implementation
- After tasks are approved and ready

**Inputs**:
- Tasks.md with all tasks
- Plan.md with architecture
- Data model and contracts
- Checklist status (if available)

**Step-by-Step process**:

1. **Check prerequisites**:
   - Run check-prerequisites script
   - Verify all required documents exist
   - Check checklist status (if checklists directory exists)
2. **Handle incomplete checklists**:
   - Display incomplete items
   - Ask user if they want to proceed anyway
   - Wait for user response before continuing
3. **Load implementation context**:
   - Read tasks.md for complete task list
   - Read plan.md for tech stack and architecture
   - Read data-model.md and contracts if exist
4. **Verify project setup**:
   - Create/verify ignore files (.gitignore, etc.)
   - Ensure proper project structure
5. **Execute tasks by phase**:
   - Complete Phase 1 (Setup) first
   - Complete Phase 2 (Foundational)
   - Execute user story phases in order
   - Complete Final Phase (Polish)
6. **Respect dependencies**:
   - Run sequential tasks in order
   - Run parallel tasks ([P] marker) concurrently
   - Don't start dependent task until prerequisite complete
7. **Track progress**:
   - Mark each task complete in tasks.md
   - Report after each task
   - Handle failures appropriately
8. **Validate completion**:
   - All tasks complete
   - Features work as specified
   - Tests pass
9. **Report final status** with summary

**Output**:
- All tasks completed and marked
- Implementation matches specification
- Final status report
- Summary of completed work

**Failure Handling**:
- Non-parallel task fails: Halt execution, report blocker
- Parallel task fails: Continue with successful tasks, report failed
- Checklists incomplete: Ask user, proceed or halt based on response
- Missing prerequisites: Block and identify missing items

---

## Skill Dependencies Graph

```
┌─────────────────────────────────────────────────────────────────┐
│                    ORCHESTRATOR (Coordinator)                    │
└──────────────────────────┬──────────────────────────────────────┘
                           │
          ┌────────────────┼────────────────┐
          ▼                ▼                ▼
   ┌──────────────┐ ┌──────────────┐ ┌──────────────┐
   │  SPEC AUTHOR │ │ PLANNING AGENT│ │TASK DECOMPOSER│
   │  (Spec Only) │ │ (Plan Only)  │ │ (Tasks Only) │
   └──────┬───────┘ └──────┬───────┘ └──────┬───────┘
          │                │                │
          └────────────────┼────────────────┘
                           ▼
               ┌───────────────────────┐
               │IMPLEMENTATION AGENT   │
               │(Implementation Only)  │
               └───────────────────────┘
```

**Flow**: Constitution → Specification → Planning → Tasks → Implementation

---

## Phase Transition Checklist

| From | To | Required Artifacts | Command |
|------|----|-------------------|---------|
| Start | Constitution | None | `/sp.constitution` |
| Constitution | Specification | `.specify/memory/constitution.md` | `/sp.specify` |
| Specification | Planning | `specs/<feature>/spec.md` | `/sp.plan` |
| Planning | Tasks | `specs/<feature>/plan.md` (+ data-model.md, contracts/) | `/sp.tasks` |
| Tasks | Implementation | `specs/<feature>/tasks.md` | `/sp.implement` |

---

## Quality Standards

All skills must adhere to these standards:

1. **Deterministic**: Same inputs produce same outputs
2. **Reusable**: Skills work across different features
3. **Traceable**: All changes trace to specifications
4. **Smallest Viability**: No over-engineering or scope creep
5. **Testable**: Each skill has clear pass/fail criteria
6. **Documented**: All decisions and assumptions recorded

---

*End of Skills Documentation*
