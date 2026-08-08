# Maestro Conventions

> The output format, naming, tag nomenclature, and agent contracts that keep the framework
> consistent across sessions, forks, and clones.
>
> See companion documents:
> - **`maestro-orchestrator-guide.md`** — dispatch matrix, handoff protocol, review pipeline.
> - **`maestro-workflow.md`** — 14-step task cycle and phase scaffolding (post-phase + maintenance).

---

## 1. Output Format: JSON + MD Hybrid (Decision A)

Every agent emits **two** files side by side for every artifact it produces:

| File | Purpose | Conforms to |
|---|---|---|
| `*.json` | Machine-parseable, structured data for CI, bot, post-processing | `.maestro-space/maestro-templates/agent-output.schema.json` |
| `*.md` | Human narrative, references the JSON for the data behind each claim | The corresponding narrative template |

**When in doubt, emit both.** Never emit only one. The JSON is for machines; the MD is
for humans; together they form the artifact.

### Where each format applies

| Artifact | JSON file | MD file |
|---|---|---|
| Activity report (per agent) | `<agent>-activity-report.json` | `<agent>-activity-report.md` |
| Reviewer findings (per phase) | `findings-phase-1.json` / `findings-phase-2.json` | `findings-phase-1.md` / `findings-phase-2.md` |
| Handoff frontmatter | embedded in `handoff.md` frontmatter (YAML); can also be emitted as `handoff.json` for tooling | `handoff.md` |
| ATDD checklist | `atdd-checklist.json` (machine-readable steps) | `atdd-checklist.md` |
| Coverage audit | `coverage-audit.json` (structured AC matrix) | `coverage-audit.md` |
| Post-phase report (per role) | `grc-report.json` etc. | `grc-report.md` etc. |
| Post-phase summary | `summary.json` | `summary.md` |
| Maintenance plan | `maintenance-phase-plan.json` | `maintenance-phase-plan.md` |

---

## 2. File Naming

### Per-task artifacts

All artifacts for a task live in the same folder:

```
.maestro-space/maestro-works/<phase-short-desc>/<task-id>-<short-desc>/
```

**Phase folder**: `phase-N-<short-description>` — kebab-case, short, descriptive.
Examples: `phase-0-delivery-system`, `phase-1-delivery-system`, `phase-2-architecture`,
`maintenance-1`, `post-phase-1`.

**Task folder**: `<task-id>-<short-description>` — task ID first (P-IDs or M-IDs),
then kebab-case short description. Examples: `p1-007-pr-template`,
`p1-021-baseline-test-fixes`, `m1-001-rotate-stale-gha-token`.

**File names** (within a task folder): `[type]-[short-desc].[ext]` matching the table
in §1 above. No agent name in the filename unless the file is a per-agent activity report.

### Per-file extension

| Extension | Use |
|---|---|
| `.json` | Machine-parseable artifact (must validate against `agent-output.schema.json`) |
| `.md` | Human-narrative artifact (must follow the matching template) |
| `.yml` / `.yaml` | Reserved for CI configuration; framework does not use YAML for runtime artifacts |

---

## 3. Tag Nomenclature (Issue Tracking)

When the orchestrator files issues for deferred, tech-debt, or SecOps findings, the title
and tag follow this strict nomenclature.

| Tag (GitHub label) | Title format | Source | Use |
|---|---|---|---|
| `Deferred` | `[Deferred.P{N}.NN]` | Review findings, low-priority | Minor changes detected by reviews that are not currently prioritized |
| `Tech Debt` | `[Tech Debt.P{N}.NN]` | Review findings, architectural/structural | Items requiring careful, expert handling |
| `SecOps` | `[SecOps.P{N}.NN]` | Red/Blue team reviews | Security findings |
| `Maintenance` | `[Maintenance.M{N}.NN]` | Post-phase session output | Maintenance phase tasks |
| `Critical` | `[Critical.P{N}.NN]` | Any source | Items that BLOCK the next phase |

**Numbering**: the `NN` is the issue number within the phase, not globally. New issues
start at `.01` per phase. Gaps in numbering are tolerated (don't reuse; let the
sequence stand).

**The Critical tag is reserved for blocking items only.** Do not over-tag. A finding
with severity `high` is not automatically Critical unless it BLOCKS the next phase.

---

## 4. Agent Contracts

Every agent (production or review) MUST satisfy these contracts:

1. **Two-file output**: every artifact is emitted as both `.json` (per
   `agent-output.schema.json`) and `.md` (per the matching template). No exceptions.
2. **Handoff update** (production agents only): the production agent updates the handoff
   frontmatter (`implementation_artifacts`, `green_phase_verified`, `head_sha`) AND writes
   the Agent Output section in the markdown body.
3. **No handoff access** (review agents only): the review agent does NOT read or update
   the handoff. It writes its findings to `findings-phase-N.{json,md}` in the task folder.
4. **Need-to-know context** (review agents only): the review agent receives only the
   diff, the spec (where applicable), and the acceptance criteria. Never the handoff,
   the plan, ADRs, or author rationale.
5. **Template adherence**: every MD file follows the matching template from
   `.maestro-space/maestro-templates/`. Every JSON file conforms to `agent-output.schema.json`.
6. **Severity assignment**: every finding is tagged `low`, `medium`, `high`, or
   `critical`. `info` is allowed for reviewer pass-through comments that are not
   actionable.
7. **File location**: every artifact lives in the task folder. The orchestrator's
   intervention is required to move anything outside the task folder.

---

## 5. JSON Schema: agent-output.schema.json

The canonical JSON schema is at `.maestro-space/maestro-templates/agent-output.schema.json`.
Every JSON file in the framework conforms to it. The schema is versioned; agents MUST
emit the `schema_version` field so future schema migrations can be detected.

The schema covers:
- `schema_version` (string, semver) — required
- `artifact_type` (enum) — required; one of: `activity-report`, `findings`,
  `atdd-checklist`, `coverage-audit`, `post-phase-report`, `post-phase-summary`,
  `maintenance-plan`, `handoff`
- `agent` (object) — required; the producing agent's name, role, and dispatch timestamp
- `task` (object) — required; the task ID, phase, branch, base_sha, head_sha
- `data` (object) — required; the artifact-specific payload, type-dependent

The schema is intentionally minimal in the top-level shape and pushes the
artifact-specific structure into `data` so the schema can evolve without breaking
existing parsers.

---

## 6. Handoff File Conventions

The handoff is the single source of truth for a task's state (spec section 15.3).
Specific conventions:

- **`status`**: must be one of `in-progress`, `review`, `coverage-audit`, `uat`, `done`,
  `blocked`. Transitions are forward-only except `blocked`, which is a halt marker.
- **`base_sha` and `head_sha`**: 40-char lowercase hex (full SHA, not abbreviated).
- **`memtrace_indexed_sha`**: must equal `head_sha` once coverage-audit step has run.
- **`pr_url`**: empty until the PR is opened (step 13). After that, the bot's PR URL.
- **`verification.*`**: all seven flags are `true` only when the task is `done`. During
  the 14-step, individual flags turn `true` as their corresponding gate passes.
- **`known_debt`**: an array of free-text entries, one per deferred/incomplete item.
  Each entry references the originating finding ID (e.g., `PH1-005`, `SEC-001`).

---

## 7. Session Handout Conventions

The session handout is the only artifact that carries state across sessions. Conventions:

- **Self-contained**: the handout must allow the next session to begin work with ZERO
  conversation history. It includes every path, every SHA, every key.
- **File location**: `.maestro-space/maestro-works/<phase>/<task>/session-handout.md`
- **Required sections**: Current State, Artifacts Produced, Pending Work, Keys For
  Next Session, Known Debt, Rollback Strategy, UAT Decision, PR Status
- **Format**: the template at `.maestro-space/maestro-templates/session-handout.md`
  defines the exact shape; deviations must be justified in the handout.

---

## 8. Secrets Handling

`maestro-secrets/` is the only place for framework-level secrets (API keys, tokens).
Rules:

- Never commit secrets to any tracked file.
- Never paste secrets into a handoff or activity report.
- Reference secrets by environment-variable name only (e.g., `$APP_PRIVATE_KEY`).
- For local development, use a `.env` file in `maestro-secrets/` (also gitignored).
- For CI, use GitHub repository secrets (preferred) or environment-bound secrets.

The `maestro-secrets/` directory is double-ignored (parent `.gitignore` plus its own
defensive `.gitignore`).

---

## 9. What Goes Where (Quick Reference)

| If it's about... | It lives in... |
|---|---|
| How the **product** is built (architecture, ADRs, specs) | `/docs/` (tracked) |
| How the **framework** works (orchestrator, workflow, conventions) | `.maestro-space/maestro-docs/` (gitignored) |
| Templates and the JSON schema | `.maestro-space/maestro-templates/` (gitignored) |
| Agent registry | `.maestro-space/maestro-agents/` (gitignored) |
| Per-phase work plans and global objectives | `.maestro-space/maestro-plans/` (gitignored) |
| Per-task session artifacts | `.maestro-space/maestro-works/<phase>/<task>/` (gitignored) |
| Workflow secrets | `.maestro-space/maestro-secrets/` (gitignored) |
| The bootstrap script itself | `scripts/maestro-bootstrap.ps1` (TRACKED — it's the only framework artifact that must be reproducible from a fresh clone) |
