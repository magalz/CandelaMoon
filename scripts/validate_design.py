#!/usr/bin/env python3
"""Validate CandelaMoon design artifacts."""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

SCHEMA_FILES = [
    "adr.schema.json",
    "evidence-manifest.schema.json",
    "capability-row.schema.json",
    "device-matrix-row.schema.json",
]

ADR_TEMPLATE = "0000-template.md"
ADR_FILE_RE = re.compile(r"^(\d{4})-(.+)\.md$")
FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*", re.DOTALL | re.MULTILINE)

MIN_NON_TRIVIAL_CHARS = 100

INFRA_REQUIRED_SECTIONS = {
    "delivery-system-design.md": [
        "# Delivery System Design",
        "## Repository",
        "## Branch",
        "## CI",
        "## Synchronization",
        "## TDD",
        "## Review",
    ],
    "ci-architecture.md": [
        "# CI Architecture",
        "## Podman",
        "## Images",
        "## Jobs",
        "## Pipeline Tiers",
    ],
    "device-lab-architecture.md": [
        "# Device Lab",
        "## Google TV Streamer",
        "## Compatibility",
        "## Fault Injection",
    ],
    "toolchain-pins.md": [
        "# Toolchain Pins",
        "## JDK",
        "## Android SDK",
        "## NDK",
        "## Gradle",
        "## Podman",
    ],
    "threat-model.md": [
        "# Threat Model",
        "## Trust Boundaries",
        "## CI",
        "## Secrets",
        "## Signing",
        "## Dependencies",
        "## Containers",
    ],
    "supply-chain-policy.md": [
        "# Supply Chain Policy",
        "## Actions",
        "## Base Images",
        "## Dependencies",
        "## SBOM",
        "## Provenance",
        "## Vulnerability",
    ],
    "secrets-and-signing-policy.md": [
        "# Secrets And Signing Policy",
        "## Secret Stores",
        "## Signing",
        "## Release",
    ],
    "incident-and-rollback-policy.md": [
        "# Incident And Rollback Policy",
        "## Bad Release",
        "## Compromised",
        "## Stale Graph",
    ],
    "retention-cache-cost-maintenance-policy.md": [
        "# Retention Cache Cost Maintenance Policy",
        "## Artifacts",
        "## Cache",
        "## Cost",
        "## Maintenance",
    ],
    "implementation-backlog.md": [
        "# Phase 1 Implementation Backlog",
        "## Work Items",
    ],
    # The implementation-backlog.md moved to .maestro-space/maestro-plans/phase-1-delivery-system-backlog.md
    # in the 2026-08-07 restructure. The validator checks the new filename + path. The
    # section headings are unchanged.
    "phase-1-delivery-system-backlog.md": [
        "# Phase 1 Implementation Backlog",
        "## Work Items",
    ],
}

try:
    import yaml
except ImportError as exc:
    yaml = None
    YAML_ERROR = (
        f"PyYAML is not installed ({exc}). Install it with: "
        f"pip install -r {Path(__file__).resolve().parent / 'requirements.txt'}"
    )
else:
    YAML_ERROR = ""

try:
    import jsonschema
    from jsonschema.exceptions import SchemaError, ValidationError
    from jsonschema.validators import validator_for
except ImportError as exc:
    jsonschema = None
    JSONSCHEMA_ERROR = (
        f"jsonschema is not installed ({exc}). Install it with: "
        f"pip install -r {Path(__file__).resolve().parent / 'requirements.txt'}"
    )
else:
    JSONSCHEMA_ERROR = ""


@dataclass
class CheckResult:
    name: str
    passed: bool
    detail: str = ""
    severity: str = "error"


@dataclass
class Report:
    results: list[CheckResult] = field(default_factory=list)

    @property
    def all_passed(self) -> bool:
        return all(r.passed for r in self.results if r.severity != "warning")

    def add(self, name: str, passed: bool, detail: str = "", severity: str = "error") -> None:
        self.results.append(CheckResult(name=name, passed=passed, detail=detail, severity=severity))


def load_schema(name: str, root: Path = REPO_ROOT) -> dict | None:
    path = root / "docs" / "schema" / name
    if not path.is_file():
        return None
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return None
    return data if isinstance(data, dict) else None


def check_schemas(report: Report, root: Path) -> None:
    for name in SCHEMA_FILES:
        path = root / "docs" / "schema" / name
        if not path.is_file():
            report.add(f"schema: {name}", False, f"missing file: {path}")
            continue
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            report.add(f"schema: {name}", False, f"invalid JSON: {exc}")
            continue
        except OSError as exc:
            report.add(f"schema: {name}", False, f"cannot read: {exc}")
            continue
        if jsonschema is None:
            report.add(f"schema: {name}", False, JSONSCHEMA_ERROR)
            continue
        try:
            validator_for(data).check_schema(data)
        except SchemaError as exc:
            report.add(f"schema: {name}", False, f"invalid JSON Schema: {exc.message}")
            continue
        except Exception as exc:
            report.add(f"schema: {name}", False, f"schema check failed: {exc}")
            continue
        report.add(f"schema: {name}", True, "valid JSON Schema")


def check_adr_frontmatter(report: Report, path: Path, root: Path) -> None:
    try:
        text = path.read_text(encoding="utf-8")
    except OSError as exc:
        report.add(f"adr: {path.name}", False, f"cannot read: {exc}")
        return
    match = FRONTMATTER_RE.match(text)
    if match is None:
        report.add(f"adr: {path.name}", False, "missing YAML frontmatter (--- delimiters)")
        return
    if yaml is None:
        report.add(f"adr: {path.name}", False, YAML_ERROR)
        return
    try:
        data = yaml.safe_load(match.group(1))
    except yaml.YAMLError as exc:
        report.add(f"adr: {path.name}", False, f"invalid YAML frontmatter: {exc}")
        return
    if not isinstance(data, dict):
        report.add(f"adr: {path.name}", False, "frontmatter must be a YAML mapping")
        return
    if jsonschema is None:
        report.add(f"adr: {path.name}", False, JSONSCHEMA_ERROR)
        return
    schema = load_schema("adr.schema.json", root=root)
    if schema is None:
        report.add(f"adr: {path.name}", False, "adr.schema.json is missing or invalid")
        return
    try:
        jsonschema.validate(data, schema)
    except ValidationError as exc:
        report.add(f"adr: {path.name}", False, f"frontmatter fails adr.schema.json: {exc.message}")
        return
    filename_match = ADR_FILE_RE.match(path.name)
    if filename_match is not None:
        filename_id = filename_match.group(1)
        if data.get("id") is not None and str(data["id"]) != filename_id:
            report.add(
                f"adr: {path.name}",
                False,
                f"filename id {filename_id} does not match frontmatter id {data['id']!r}",
                severity="warning",
            )
            return
    report.add(f"adr: {path.name}", True, "frontmatter validates against adr.schema.json")


def check_adrs(report: Report, root: Path) -> None:
    adr_dir = root / "docs" / "adr"
    if not adr_dir.is_dir():
        report.add("adr: directory", False, f"missing directory: {adr_dir}")
        return
    adr_files: list[Path] = []
    for path in sorted(adr_dir.iterdir()):
        if not path.is_file() or path.suffix != ".md":
            continue
        if path.name.startswith("0000"):
            continue
        if ADR_FILE_RE.match(path.name) is None:
            report.add(
                f"adr: unexpected file {path.name}",
                False,
                "file does not match NNNN-name.md",
                severity="warning",
            )
            continue
        adr_files.append(path)
    if not adr_files:
        report.add("adr: files", False, f"no ADR files found in {adr_dir}")
        return
    for path in adr_files:
        check_adr_frontmatter(report, path, root)
    check_adr_ids(report, adr_files)


def check_adr_ids(report: Report, adr_files: list[Path]) -> None:
    ids: list[int] = []
    for path in adr_files:
        match = ADR_FILE_RE.match(path.name)
        if match is not None:
            ids.append(int(match.group(1)))
    if not ids:
        report.add("adr: sequential ids", False, "no ADR files found")
        return
    expected = list(range(1, len(ids) + 1))
    if ids != expected:
        missing = [i for i in expected if i not in ids]
        duplicates = [i for i in sorted(set(ids)) if ids.count(i) > 1]
        details = []
        if missing:
            details.append("missing: " + ", ".join(f"{i:04d}" for i in missing))
        if duplicates:
            details.append("duplicates: " + ", ".join(f"{i:04d}" for i in duplicates))
        actual = ", ".join(f"{i:04d}" for i in ids)
        details.append(f"found: {actual}")
        report.add("adr: sequential ids", False, "; ".join(details))
        return
    report.add("adr: sequential ids", True, f"0001..{len(ids):04d} in order")


def check_adr_template(report: Report, root: Path) -> None:
    path = root / "docs" / "adr" / ADR_TEMPLATE
    if path.is_file():
        report.add("adr: template", True, f"{ADR_TEMPLATE} exists")
    else:
        report.add("adr: template", False, f"missing: {path}")


def check_infra_docs(report: Report, root: Path) -> None:
    for name in INFRA_REQUIRED_SECTIONS:
        # The Phase 1 implementation backlog moved to .maestro-space/maestro-plans/
        # in the 2026-08-07 restructure (file renamed to phase-1-delivery-system-backlog.md).
        # The validator checks the new location; if not found, it falls back to the old
        # location with a deprecation note.
        if name == "implementation-backlog.md":
            new_path = root / ".maestro-space" / "maestro-plans" / "phase-1-delivery-system-backlog.md"
            old_path = root / "docs" / "infrastructure" / name
            if new_path.is_file():
                path = new_path
            elif old_path.is_file():
                path = old_path
            else:
                report.add(
                    f"infra: {name}",
                    False,
                    f"missing file at both new ({new_path}) and old ({old_path}) locations",
                )
                continue
        elif name == "phase-1-delivery-system-backlog.md":
            # New maestro location for the Phase 1 implementation backlog.
            path = root / ".maestro-space" / "maestro-plans" / name
        else:
            path = root / "docs" / "infrastructure" / name
        if not path.is_file():
            report.add(f"infra: {name}", False, f"missing file: {path}")
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except OSError as exc:
            report.add(f"infra: {name}", False, f"cannot read: {exc}")
            continue
        content_len = len("".join(text.split()))
        if content_len < MIN_NON_TRIVIAL_CHARS:
            report.add(
                f"infra: {name}",
                False,
                f"non-trivial content check failed: {content_len} non-whitespace characters "
                f"(min {MIN_NON_TRIVIAL_CHARS})",
            )
            continue
        report.add(f"infra: {name}", True, f"exists, {content_len} non-whitespace characters")


def check_infra_sections(report: Report, root: Path) -> None:
    for name, required in INFRA_REQUIRED_SECTIONS.items():
        # Same new-location fallback for the implementation-backlog.
        if name == "implementation-backlog.md":
            new_path = root / ".maestro-space" / "maestro-plans" / "phase-1-delivery-system-backlog.md"
            old_path = root / "docs" / "infrastructure" / name
            if new_path.is_file():
                path = new_path
            elif old_path.is_file():
                path = old_path
            else:
                report.add(
                    f"sections: {name}",
                    False,
                    f"missing file at both new ({new_path}) and old ({old_path}) locations",
                )
                continue
        elif name == "phase-1-delivery-system-backlog.md":
            path = root / ".maestro-space" / "maestro-plans" / name
        else:
            path = root / "docs" / "infrastructure" / name
        if not path.is_file():
            report.add(f"sections: {name}", False, f"missing file: {path}")
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except OSError as exc:
            report.add(f"sections: {name}", False, f"cannot read: {exc}")
            continue
        headings = {line.rstrip() for line in text.splitlines()}
        missing = [heading for heading in required if heading not in headings]
        if missing:
            report.add(f"sections: {name}", False, "missing headings: " + ", ".join(missing))
        else:
            report.add(f"sections: {name}", True, f"all {len(required)} required headings present")


def run_checks(root: Path) -> Report:
    report = Report()
    check_schemas(report, root)
    check_adrs(report, root)
    check_adr_template(report, root)
    check_infra_docs(report, root)
    check_infra_sections(report, root)
    return report


def print_report(report: Report, strict: bool) -> None:
    for result in report.results:
        if result.severity == "warning":
            print(f"[WARN] {result.name}: {result.detail}")
        elif result.passed:
            print(f"[PASS] {result.name}: {result.detail}")
        else:
            print(f"[FAIL] {result.name}: {result.detail}")
    passed = sum(1 for r in report.results if r.severity != "warning" and r.passed)
    failed = sum(1 for r in report.results if r.severity != "warning" and not r.passed)
    warned = sum(1 for r in report.results if r.severity == "warning")
    plural = "s" if warned != 1 else ""
    print()
    print(f"Summary: {passed} passed, {failed} failed, {warned} warning{plural} ({len(report.results)} checks)")
    if failed or (strict and warned):
        print("RESULT: FAIL")
    else:
        print("RESULT: PASS")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate CandelaMoon design artifacts.")
    parser.add_argument("--strict", action="store_true", help="treat warnings as failures")
    parser.add_argument(
        "--repo-root",
        type=Path,
        default=REPO_ROOT,
        help=f"repository root (default: parent of the scripts directory: {REPO_ROOT})",
    )
    args = parser.parse_args(argv)
    report = run_checks(args.repo_root)
    print_report(report, args.strict)
    if report.all_passed and not (args.strict and any(r.severity == "warning" for r in report.results)):
        return 0
    return 1


if __name__ == "__main__":
    sys.exit(main())
