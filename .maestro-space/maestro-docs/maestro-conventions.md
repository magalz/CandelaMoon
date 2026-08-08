# Maestro Conventions

> The output format, naming, tag nomenclature, and agent contracts that keep the
> framework consistent across sessions, forks, and clones.
>
> See companion documents:
> - **`maestro-orchestrator-guide.md`** — dispatch matrix, handoff protocol, review pipeline.
> - **`maestro-workflow.md`** — task cycle and phase scaffolding.
> - **`maestro-setup.md`** — rules for the phase setup session.
> - **`maestro-post-phase.md`** — rules for post-phase execution.
> - **`maestro-maintenance.md`** — rules for maintenance phase execution.

---

## 1. Output Format: JSON + MD Hybrid (Decision A)

Every agent emits TWO files side by side for every artifact:

| File | Purpose |
|---|---|
| `*.json` | Machine-parseable, structured data for CI, bots, post-processing |
| `*.md` | Human narrative, references the JSON for data behind each claim |

**When in doubt, emit both.** The JSON is for machines; the MD is for humans.

### Per-Artifact Mapping

| Artifact | JSON file | MD file |
|---|---|---|
| Activity report | `<name>-activity-report.json` | `<name>-activity-report.md` |
| Reviewer findings | `findings-phase-1.json` / `findings-phase-2.json` | `findings-phase-1.md` / `findings-phase-2.md` |
| Handoff frontmatter | Embedded in handoff YAML | `handoff.md` |
| ATDD checklist | `atdd-checklist.json` | `atdd-checklist.md` |
| Coverage audit | `coverage-audit.json` | `coverage-audit.md` |
| Post-phase report | `<role>-report.json` | `<role>-report.md` |
| Post-phase summary | `summary.json` | `summary.md` |
| Maintenance plan | `maintenance-phase-plan.json` | `maintenance-phase-plan.md` |

---

## 2. File Naming

### Per-task artifacts

All artifacts for a task live in the same task workspace folder.

**Phase folder**: `phase-N-<short-description>` — kebab-case, short, descriptive.

**Task folder**: `<task-id>-<short-description>` — task ID first, then kebab-case.

**Agent files**: `[name]-[role].md` — e.g., `bernstein-orchestrator.md`, `bach-senior-developer.md`.

### Extensions

| Extension | Use |
|---|---|
| `.json` | Machine-parseable artifact |
| `.md` | Human-narrative artifact |
| `.yml` / `.yaml` | Reserved for CI configuration |

---

## 3. Tag Nomenclature (Issue Tracking)

| Tag | Title format | Source | Use |
|---|---|---|---|
| `Deferred` | `[Deferred.P{N}.NN]` | Review findings, low-priority | Minor changes, not currently prioritized |
| `Tech Debt` | `[Tech Debt.P{N}.NN]` | Review findings, architectural | Items requiring careful, expert handling |
| `SecOps` | `[SecOps.P{N}.NN]` | Red/Blue team reviews | Security findings |
| `Maintenance` | `[Maintenance.M{N}.NN]` | Post-phase session output | Maintenance phase tasks |
| `Critical` | `[Critical.P{N}.NN]` | Any source | Items that BLOCK the next phase |

**Numbering**: `NN` is the issue number within the phase, not globally. Gaps are tolerated.

---

## 4. Agent Contracts

Every agent MUST satisfy these contracts:

1. **Two-file output**: every artifact is emitted as both `.json` and `.md`. No exceptions.
2. **Handoff update** (production agents only): update `implementation_artifacts`,
   `green_phase_verified`, `head_sha`, and the Agent Output section.
3. **No handoff access** (review agents only): never read or update the handoff. Write
   findings to `findings-phase-N.{json,md}` in the task folder.
4. **Need-to-know context** (review agents only): receive only the diff, spec (where
   applicable), and acceptance criteria. Never the handoff, plan, ADRs, or author rationale.
5. **Template adherence**: every MD file follows the matching template. Every JSON file
   conforms to the agent-output schema.
6. **Severity assignment**: every finding tagged `low`, `medium`, `high`, or `critical`.
7. **File location**: every artifact lives in the task folder.

---

## 5. Handoff File Conventions

- **`status`**: one of `in-progress`, `review`, `coverage-audit`, `uat`, `done`, `blocked`.
  Transitions are forward-only except `blocked`.
- **`base_sha` and `head_sha`**: 40-char lowercase hex (full SHA).
- **`memtrace_indexed_sha`**: must equal `head_sha` once coverage-audit has run.
- **`pr_url`**: empty until the PR is opened.
- **`known_debt`**: array of free-text entries, each referencing the originating finding ID.

---

## 6. Session Handout Conventions

- **Self-contained**: must allow the next session to begin with ZERO conversation history.
- **Required sections**: Current State, Artifacts Produced, Pending Work, Keys For
  Next Session, Known Debt, Rollback Strategy.

---

## 7. Secrets Handling

- Never commit secrets to any tracked file.
- Never paste secrets into a handoff or activity report.
- Reference secrets by environment-variable name only (e.g., `$APP_PRIVATE_KEY`).
- For local development, use a `.env` file in the secrets directory (gitignored).
- For CI, use repository secrets or environment-bound secrets.

---

## 8. What Goes Where

| If it's about... | It lives in... |
|---|---|
| How the **product** is built (architecture, ADRs, specs) | `/docs/` (tracked) |
| How the **framework** works (orchestrator, workflow, conventions) | Framework docs directory (versioned with the framework) |
| Templates and the JSON schema | Templates directory |
| Agent registry and individual agent files | Agents directory |
| Per-phase work plans and global objectives | Plans directory |
| Per-task session artifacts | Works directory |
| Workflow secrets | Secrets directory (gitignored) |
