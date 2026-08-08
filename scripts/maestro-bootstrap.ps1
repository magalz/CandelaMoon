<#
.SYNOPSIS
    Bootstrap the .maestro-space/ orchestration framework on a fresh clone.

.DESCRIPTION
    Creates the .maestro-space/ directory tree (gitignored) and a starter set of files
    (index.md, .gitignore, .gitkeep markers). Does NOT populate the framework content
    itself — each fork/clone owner is expected to maintain their own framework under
    .maestro-space/.

    The framework is per-fork by design: each person or team that works the repo
    maintains their own orchestrator guide, workflow, conventions, templates, and
    agent manifest under .maestro-space/. The scripts/ directory is the only
    framework artifact that is TRACKED, so the bootstrap mechanism is reproducible
    across clones.

    After running this script, populate the framework by either:
      1. Copying the framework files from a sibling clone of the same fork
      2. Authoring new framework files for your own orchestrator/workflow/conventions
      3. Downloading a framework bundle from your fork's release/tag

.PARAMETER RepoRoot
    The repository root. Defaults to the current working directory.

.EXAMPLE
    PS> .\scripts\maestro-bootstrap.ps1

.EXAMPLE
    PS> .\scripts\maestro-bootstrap.ps1 -RepoRoot 'D:\Repos\CandelaMoon'

.NOTES
    Idempotent: re-running on an already-bootstrapped .maestro-space/ is safe; the
    script only creates missing directories and starter files. It does NOT overwrite
    existing framework files.
#>

[CmdletBinding()]
param(
    [string]$RepoRoot = (Get-Location).Path
)

$ErrorActionPreference = 'Stop'

# --- Resolve and validate the repo root ----------------------------------------

$RepoRoot = (Resolve-Path -LiteralPath $RepoRoot).Path
if (-not (Test-Path -LiteralPath (Join-Path $RepoRoot '.git'))) {
    throw "RepoRoot '$RepoRoot' is not a git repository (no .git directory found)."
}

# --- Compute paths -------------------------------------------------------------

$MaestroSpace = Join-Path $RepoRoot '.maestro-space'
$IndexPath    = Join-Path $MaestroSpace 'index.md'
$GitignorePath = Join-Path $MaestroSpace '.gitignore'

$Subdirs = @(
    'maestro-docs'
    'maestro-plans'
    'maestro-works'
    'maestro-secrets'
    'maestro-templates'
    'maestro-agents'
)

# --- Ensure parent .gitignore entry -------------------------------------------

$ParentGitignore = Join-Path $RepoRoot '.gitignore'
$ParentEntry = '.maestro-space/'
$ParentDirty = $false
if (Test-Path -LiteralPath $ParentGitignore) {
    $existing = Get-Content -LiteralPath $ParentGitignore -Raw
    if ($existing -notmatch [regex]::Escape($ParentEntry)) {
        Add-Content -LiteralPath $ParentGitignore -Value $ParentEntry
        $ParentDirty = $true
    }
} else {
    Set-Content -LiteralPath $ParentGitignore -Value $ParentEntry
    $ParentDirty = $true
}

# --- Create the .maestro-space/ tree -------------------------------------------

$createdDirs = @()
$existingDirs = @()
foreach ($sub in $Subdirs) {
    $p = Join-Path $MaestroSpace $sub
    if (-not (Test-Path -LiteralPath $p)) {
        New-Item -ItemType Directory -Force -Path $p | Out-Null
        $createdDirs += $sub
    } else {
        $existingDirs += $sub
    }
}

# --- Marker files (idempotent) -------------------------------------------------

$markers = @(
    @{ Path = (Join-Path $MaestroSpace 'maestro-works' '.gitkeep'); Content = "# Marker — maestro-works is per-task session artifacts, never tracked.`n# Per-task folders are created at session start and live only for that task's session.`n" }
    @{ Path = (Join-Path $MaestroSpace 'maestro-secrets' '.gitkeep'); Content = "# Marker — maestro-secrets holds workflow secrets (API keys, tokens, etc.).`n# This directory is NEVER tracked. Access is restricted to the orchestrator at runtime.`n" }
)
$markersCreated = @()
$markersExisting = @()
foreach ($m in $markers) {
    if (-not (Test-Path -LiteralPath $m.Path)) {
        Set-Content -LiteralPath $m.Path -Value $m.Content -Encoding UTF8
        $markersCreated += Split-Path -Leaf (Split-Path -Parent $m.Path) + '/.gitkeep'
    } else {
        $markersExisting += Split-Path -Leaf (Split-Path -Parent $m.Path) + '/.gitkeep'
    }
}

# --- Internal .gitignore (defensive) -------------------------------------------

$InternalGitignore = @'
# Defensive .gitignore for .maestro-space/
# The parent .gitignore already excludes the entire .maestro-space/ directory.
# This file exists so that:
#   1. Per-fork clones that may not have the parent .gitignore still keep this dir out
#   2. Anyone inspecting the structure can see what is and is not tracked
#   3. Future tools that respect per-directory .gitignore behave correctly

# Everything in this directory is framework-local and must never be committed.
*
!/index.md
!/.gitignore

# Allow folder structure placeholders to exist (markers, not artifacts)
!/.gitkeep
!/*/
!/*/.gitkeep

# But never the contents of the runtime/working folders
/maestro-secrets/*
/maestro-works/**/*
!/maestro-works/.gitkeep
!/maestro-works/*/
!/maestro-works/*/.gitkeep
'@

if (-not (Test-Path -LiteralPath $GitignorePath)) {
    Set-Content -LiteralPath $GitignorePath -Value $InternalGitignore -Encoding UTF8
} else {
    Write-Verbose "Existing .maestro-space/.gitignore found; not overwriting."
}

# --- Starter index.md (idempotent — only writes if missing) -------------------

$IndexContent = @'
# `.maestro-space/`

> The orchestration framework's local runtime and authoring workspace. **Gitignored.**
> This directory is per-fork and per-clone — each framework owner maintains their own copy.
> Nothing inside this directory is pushed to a remote.

## Status

This `.maestro-space/` was scaffolded by `scripts/maestro-bootstrap.ps1` on <DATE>.
The framework files have not yet been populated. See `scripts/maestro-bootstrap.ps1`
for the source-of-truth bootstrap mechanism.

To populate the framework for your fork, either:
1. Copy the framework files from a sibling clone of the same fork
2. Author new framework files for your own orchestrator/workflow/conventions
3. Download a framework bundle from your fork's release/tag

## Layout (scaffolded)

```
.maestro-space/
├── index.md                              ← this file
├── .gitignore                            ← defensive internal excludes
├── maestro-docs/                         ← framework reference documents
├── maestro-plans/                        ← framework plans (work in progress)
├── maestro-works/                        ← per-task session artifacts
├── maestro-secrets/                      ← workflow secrets (never tracked)
├── maestro-templates/                    ← all reusable templates
└── maestro-agents/                       ← agent registry
```

## Relationship to `/docs/`

- **`/docs/`** — project documentation (architecture, ADRs, specs, test suites, schemas)
- **`.maestro-space/`** — framework files (orchestrator, workflow, conventions, templates, plans)

If a file describes **how the product is built** → it lives in `/docs/`.
If a file describes **how the framework orchestrates the work** → it lives in `.maestro-space/`.
'@

$IndexContent = $IndexContent.Replace('<DATE>', (Get-Date -Format 'yyyy-MM-dd'))
$indexCreated = $false
if (-not (Test-Path -LiteralPath $IndexPath)) {
    Set-Content -LiteralPath $IndexPath -Value $IndexContent -Encoding UTF8
    $indexCreated = $true
}

# --- Report --------------------------------------------------------------------

Write-Host ""
Write-Host "=== maestro-bootstrap ===" -ForegroundColor Cyan
Write-Host "Repo root:           $RepoRoot"
Write-Host ".maestro-space/:     $MaestroSpace"
if ($ParentDirty) {
    Write-Host "  - parent .gitignore: added '.maestro-space/'" -ForegroundColor Yellow
} else {
    Write-Host "  - parent .gitignore: '.maestro-space/' already present"
}
if ($createdDirs.Count -gt 0) {
    Write-Host "  - created subdirs:  $($createdDirs -join ', ')" -ForegroundColor Green
} else {
    Write-Host "  - subdirs:          all present (idempotent)"
}
if ($existingDirs.Count -gt 0) {
    Write-Host "  - existing subdirs: $($existingDirs -join ', ')"
}
if ($indexCreated) {
    Write-Host "  - index.md:          created (starter; needs framework content)" -ForegroundColor Green
} else {
    Write-Host "  - index.md:          already present (not overwritten)"
}
if ($markersCreated.Count -gt 0) {
    Write-Host "  - markers created:   $($markersCreated -join ', ')" -ForegroundColor Green
}
if ($markersExisting.Count -gt 0) {
    Write-Host "  - markers existing:  $($markersExisting -join ', ')"
}
if (-not (Test-Path -LiteralPath $GitignorePath)) {
    Write-Host "  - .gitignore:        created (defensive internal excludes)" -ForegroundColor Green
} else {
    Write-Host "  - .gitignore:        already present (not overwritten)"
}
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Cyan
Write-Host "  1. Populate .maestro-space/ with your fork's framework files"
Write-Host "     (orchestrator guide, workflow, conventions, templates, agent manifest)."
Write-Host "  2. Start your first task session by reading the orchestrator guide and creating"
Write-Host "     .maestro-space/maestro-works/<phase>/<task-id>-<short-desc>/handoff.md."
Write-Host ""
Write-Host "Bootstrap complete." -ForegroundColor Cyan
