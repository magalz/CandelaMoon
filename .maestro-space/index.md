# `.maestro-space/`

> The orchestration framework's local runtime and authoring workspace. **Gitignored.**
> This directory is per-fork and per-clone — each framework owner maintains their own copy.
> Nothing inside this directory is pushed to a remote.

## Purpose

`.maestro-space/` is the home for **all** framework files — orchestrator guide, workflow
definitions, conventions, templates, agent registry, phase plans, and per-task session
artifacts. `/docs/` is reserved for **project documentation only** (architecture, ADRs,
specs, test suites, schemas). The two namespaces never overlap.

## Layout

```
.maestro-space/
├── index.md                              ← you are here
├── .gitignore                            ← defensive internal excludes (parent also ignores this dir)
│
├── maestro-docs/                         ← framework reference documents
│   ├── maestro-orchestrator-guide.md     ← dispatch matrix, handoff protocol, review pipeline
│   ├── maestro-workflow.md               ← 14-step task cycle + phase scaffolding (post-phase + maintenance)
│   └── maestro-conventions.md            ← JSON+MD output format, naming, tag nomenclature, agent contracts
│
├── maestro-plans/                        ← framework plans (work in progress)
│   ├── global-objectives.md              ← north star, phase strategy
│   └── phase-N-<short-desc>-backlog.md   ← per-phase task list (P-IDs)
│
├── maestro-works/                        ← per-task session artifacts (1 task = 1 folder = 1 PR)
│   └── <phase>-<short-desc>/
│       └── <task-id>-<short-desc>/
│           ├── handoff.md
│           ├── atdd-checklist.md
│           ├── coverage-audit.md
│           ├── session-handout.md
│           ├── findings-phase-1.json     ← machine-readable
│           ├── findings-phase-1.md       ← human narrative
│           ├── findings-phase-2.json
│           ├── findings-phase-2.md
│           ├── <agent>-activity-report.json
│           └── <agent>-activity-report.md
│
├── maestro-secrets/                      ← workflow secrets (API keys, tokens) — never tracked
│
├── maestro-templates/                    ← all reusable templates (handoff, PR, issues, post-phase, etc.)
│   ├── agent-output.schema.json          ← canonical JSON schema for every agent's structured output
│   ├── handoff.md
│   ├── atdd-checklist.md
│   ├── coverage-audit.md
│   ├── session-handout.md
│   ├── post-phase-grc.md
│   ├── post-phase-qa.md
│   ├── post-phase-security.md
│   ├── post-phase-devops.md
│   ├── post-phase-summary.md
│   ├── maintenance-phase-plan.md
│   ├── issue-deferred.md
│   ├── issue-tech-debt.md
│   ├── issue-secops.md
│   ├── pr.md
│   ├── agent-activity-report.md
│   └── agent-findings-report.md
│
└── maestro-agents/                       ← agent registry
    └── agent-manifest.json               ← name, subagent_type, role, dispatch matrix
```

## Relationship to `/docs/`

- **`/docs/`** — **project documentation**, tracked, pushed to the remote. Reserved for:
  - ADRs (architectural decisions about the **product**)
  - Specs and plans (the **product** spec at `docs/superpowers/specs/`, the **product** plan at `docs/superpowers/plans/`)
  - Test suite documentation
  - Architecture files
  - Project schemas (`docs/schema/`)
- **`.maestro-space/`** — **framework files**, gitignored, local-only. Contains everything
  about how the orchestrator and agents work, including the templates and conventions they use.

If a file describes **how the product is built** → it lives in `/docs/`.
If a file describes **how the framework orchestrates the work** → it lives in `.maestro-space/`.

## Bootstrap

After a fresh clone, run from the repo root:

```powershell
.\scripts\maestro-bootstrap.ps1
```

The script creates this directory tree and the `.gitignore` entries that keep the
framework files out of the project's tracked set. The tracked counterpart of the
bootstrap mechanism is the script itself at `scripts/maestro-bootstrap.ps1`.

## Workflow in one sentence

**One task = one session = one PR (14-step cycle). One phase = N task sessions +
one post-phase session (4 architects) + one maintenance phase (N tasks).**
See `maestro-docs/maestro-workflow.md` for the full contract.
