# `.maestro-space/`

> The orchestration framework's local runtime and authoring workspace. **Gitignored.**
> This directory is per-fork and per-clone — each framework owner maintains their own copy.
> Nothing inside this directory is pushed to a remote.

## Purpose

`.maestro-space/` is the home for **all** framework files — orchestrator guide, workflow
definitions, conventions, templates, agent registry, phase plans, and per-task session
artifacts. `/docs/` is reserved for **project documentation only**. The two namespaces
never overlap.

## Layout

```
.maestro-space/
├── index.md                              ← you are here
├── .gitignore                            ← defensive internal excludes (parent also ignores this dir)
│
├── maestro-docs/                         ← framework reference documents
│   ├── maestro-orchestrator-guide.md     ← dispatch matrix, handoff protocol, review pipeline
│   ├── maestro-workflow.md               ← 14-step task cycle + phase scaffolding (post-phase + maintenance)
│   ├── maestro-setup.md                  ← rules for the phase setup session
│   ├── maestro-post-phase.md             ← rules for post-phase execution
│   ├── maestro-maintenance.md            ← rules for maintenance phase execution
│   └── maestro-conventions.md            ← JSON+MD output format, naming, tag nomenclature, agent contracts
│
├── maestro-plans/                        ← framework plans (work in progress)
│   ├── global-objectives.md              ← north star, phase strategy (global)
│   ├── master-roadmap.md                 ← high-level phase guide (global)
│   ├── phase-0-delivery-system/
│   │   └── backlog.md                    ← per-phase task list (P-IDs)
│   ├── phase-1-delivery-system/
│   │   └── backlog.md
│   └── phase-N-<short-desc>/
│       └── backlog.md
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
│   ├── handoff.md                        ← task handoff template
│   ├── atdd-checklist.md                 ← TDD red-phase checklist
│   ├── coverage-audit.md                 ← standalone coverage audit
│   ├── session-handout.md                ← per-task session handout
│   ├── phase-plan.md                     ← per-phase master plan
│   ├── task-file.md                      ← individual task file
│   ├── setup-handout.md                  ← phase setup handout
│   ├── post-phase-grc.md                 ← post-phase governance report
│   ├── post-phase-qa.md                  ← post-phase quality report
│   ├── post-phase-security.md            ← post-phase security report
│   ├── post-phase-devops.md              ← post-phase devops report
│   ├── post-phase-summary.md             ← post-phase synthesized summary
│   ├── post-phase-handout.md             ← post-phase continuity handout
│   ├── maintenance-phase-plan.md         ← maintenance phase task plan
│   ├── maintenance-completion-handout.md ← maintenance completion handout
│   ├── pr.md                             ← pull request description
│   ├── agent-activity-report.md          ← per-agent activity report
│   ├── agent-findings-report.md          ← reviewer findings report
│   ├── issue-deferred.md                 ← deferred issue
│   ├── issue-tech-debt.md                ← tech debt issue
│   └── issue-secops.md                   ← security issue
│
└── maestro-agents/                       ← agent registry (definitive source of truth)
    ├── agent-manifest.json               ← full registry: names, roles, dispatch matrix
    ├── bernstein-orchestrator.md         ← Bernstein (Principal Orchestrator)
    ├── bach-senior-developer.md          ← Bach (Code Implementation)
    ├── ravel-qa-architect.md             ← Ravel (TDD & Coverage Audit)
    ├── vivaldi-devops-architect.md       ← Vivaldi (CI & Infrastructure)
    ├── paganini-security-analyst.md      ← Paganini (Threat Modeling & Security Design)
    ├── haydn-grc-architect.md            ← Haydn (ADR Governance & Compliance)
    ├── schubert-tech-writer.md           ← Schubert (Documentation & Session Handouts)
    ├── debussy-ux-ui-designer.md         ← Debussy (UI/UX Design & Accessibility)
    ├── berlioz-blind-hunter.md           ← Berlioz (Phase 1 Adversarial Review)
    ├── bartok-edge-case-hunter.md        ← Bartók (Phase 1 Edge Case & Boundary Review)
    ├── verdi-acceptance-analyst.md       ← Verdi (Phase 1 Acceptance Review)
    ├── stravinsky-red-team-analyst.md    ← Stravinsky (Phase 2 Offensive Security)
    └── brahms-blue-team-analyst.md       ← Brahms (Phase 2 Defensive Security)
```

## Relationship to `/docs/`

- **`/docs/`** — **project documentation**, tracked, pushed to the remote. Reserved for
  ADRs, specs, plans, test documentation, architecture files, and project schemas.
- **`.maestro-space/`** — **framework files**, local-only. Contains everything
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
