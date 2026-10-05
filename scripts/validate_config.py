#!/usr/bin/env python3
"""Check that the job-application repository is internally consistent."""

from __future__ import annotations

import json
import py_compile
import re
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]

REQUIRED_FILES = (
    "AGENTS.md",
    ".cursor/environment.json",
    ".cursor/rules/job-application-agent.mdc",
    "config/master_profile.md",
    "config/job_preferences.md",
    "config/application_rules.md",
    "config/job_scoring.md",
    "config/resume_tailoring.md",
    "config/answer_bank.md",
    "config/red_flags.md",
    "config/site_policy.md",
    "config/mcp_setup.md",
    "config/runtime.md",
    "config/target_config_block.md",
    "data/application_tracker.csv",
    "prompts/daily_automation_prompt.md",
    "templates/daily_report.md",
    "scripts/build_resume_pdf.py",
    "scripts/resume_schema.json",
    "scripts/validate_config.py",
    "reference/Karina_Rohra_Digital_Marketing_Resume_FINAL.pdf",
    "requirements.txt",
)

FORBIDDEN_ROOT_FILES = (
    "master_profile.md",
    "job_preferences.md",
    "application_rules.md",
    "job_scoring.md",
    "resume_tailoring.md",
    "answer_bank.md",
    "red_flags.md",
    "site_policy.md",
    "mcp_setup.md",
    "runtime.md",
    "target_config_block.md",
    "application_tracker.csv",
    "daily_automation_prompt.md",
    "daily_report.md",
    "job-application-agent.mdc",
    "Karina_Rohra_Digital_Marketing_Resume_FINAL.pdf",
    "Karina_Rohra_Digital_Marketing_Resume(1).pdf",
    "Cursor_Job_Application_Agent_FINAL.zip",
)

PIPELINE = (
    "validate configuration",
    "discover jobs",
    "deduplicate",
    "filter",
    "score",
    "tailor resume",
    "generate real PDF",
    "validate PDF",
    "prepare application",
    "hard-stop where required",
    "submit only in LIVE mode",
    "update Google Sheets",
    "generate report",
)

PATH_PATTERN = re.compile(
    r"(?:config|data|scripts|reference|prompts|templates|\.cursor)/[A-Za-z0-9_./-]+\.[A-Za-z0-9]+"
)

SECRET_PATTERN = re.compile(
    r"(?i)\b(?:api[_-]?key|secret|password|access[_-]?token|refresh[_-]?token|otp|session[_-]?token)\b\s*[:=]\s*['\"]?[A-Za-z0-9_\-.]{8,}"
)

TEXT_SUFFIXES = {".md", ".mdc", ".json", ".csv", ".txt", ".py"}


def read(relative: str) -> str:
    return (REPO_ROOT / relative).read_text(encoding="utf-8")


def setting(text: str, name: str) -> str | None:
    match = re.search(rf"(?m)^{re.escape(name)}=(.*)$", text)
    if not match:
        return None
    return match.group(1).strip()


def main() -> int:
    failures: list[str] = []

    def check(condition: bool, message: str) -> None:
        if condition:
            print(f"PASS  {message}")
        else:
            failures.append(message)
            print(f"FAIL  {message}")

    for relative in REQUIRED_FILES:
        check((REPO_ROOT / relative).is_file(), f"required file exists: {relative}")

    for name in FORBIDDEN_ROOT_FILES:
        check(not (REPO_ROOT / name).exists(), f"stale root file absent: {name}")

    runtime = read("config/runtime.md") if (REPO_ROOT / "config/runtime.md").is_file() else ""
    mode = setting(runtime, "RUN_MODE")
    check(mode in {"REVIEW_ONLY", "LIVE"}, f"RUN_MODE is REVIEW_ONLY or LIVE (found {mode})")
    if mode == "REVIEW_ONLY":
        print("PASS  current RUN_MODE=REVIEW_ONLY")
    check(setting(runtime, "MAX_APPLICATIONS_PER_RUN") == "5", "MAX_APPLICATIONS_PER_RUN=5")
    check(setting(runtime, "MAX_APPLICATIONS_PER_DAY") == "10", "MAX_APPLICATIONS_PER_DAY=10")
    check(setting(runtime, "AUTO_APPLY_THRESHOLD") == "85", "AUTO_APPLY_THRESHOLD=85")
    check(
        setting(runtime, "AUTHORITATIVE_RESUME")
        == "reference/Karina_Rohra_Digital_Marketing_Resume_FINAL.pdf",
        "authoritative resume path is the final PDF",
    )
    check(setting(runtime, "TRACKER_AUTHORITY") == "google_sheets", "Google Sheets is the tracker authority")
    check(
        setting(runtime, "TRACKER_CACHE") == "data/application_tracker.csv",
        "GitHub CSV is marked as the backup cache",
    )
    check(setting(runtime, "SPREADSHEET_ID") is not None, "SPREADSHEET_ID is present")

    rules = read("config/application_rules.md") if (REPO_ROOT / "config/application_rules.md").is_file() else ""
    scoring = read("config/job_scoring.md") if (REPO_ROOT / "config/job_scoring.md").is_file() else ""
    preferences = read("config/job_preferences.md") if (REPO_ROOT / "config/job_preferences.md").is_file() else ""
    prompt = (
        read("prompts/daily_automation_prompt.md")
        if (REPO_ROOT / "prompts/daily_automation_prompt.md").is_file()
        else ""
    )
    profile = read("config/master_profile.md") if (REPO_ROOT / "config/master_profile.md").is_file() else ""

    check("RUN_MODE=REVIEW_ONLY" in rules, "application rules keep REVIEW_ONLY")
    check("Never submit an application." in rules, "application rules forbid submission in review mode")
    check("Never click a final Submit" in rules, "application rules forbid the final submit control")
    check("AUTO_APPLY_THRESHOLD=85" in rules and "AUTO_APPLY_THRESHOLD=85" in scoring, "threshold 85 is consistent")
    check("MAX_APPLICATIONS_PER_RUN=5" in preferences, "per-run cap is consistent")
    check("MAX_APPLICATIONS_PER_DAY=10" in preferences, "per-day cap is consistent")
    check(
        "Source resume filename: Karina_Rohra_Digital_Marketing_Resume_FINAL.pdf" in profile,
        "master profile names the final resume",
    )
    check(
        "Source resume filename: Karina_Rohra_Digital_Marketing_Resume(1).pdf" not in profile,
        "master profile does not treat the older resume as the source",
    )
    check("Google Sheets" in rules and "backup cache" in rules.lower(), "deduplication does not rely only on git")

    folded_prompt = prompt.casefold()
    cursor = 0
    pipeline_ok = True
    for stage in PIPELINE:
        index = folded_prompt.find(stage.casefold(), cursor)
        if index < 0:
            pipeline_ok = False
            break
        cursor = index + len(stage)
    check(pipeline_ok, "daily prompt follows the required pipeline order")

    referenced: set[str] = set()
    for relative in (
        "AGENTS.md",
        "config/runtime.md",
        "config/application_rules.md",
        "config/resume_tailoring.md",
        "config/mcp_setup.md",
        "prompts/daily_automation_prompt.md",
        ".cursor/rules/job-application-agent.mdc",
    ):
        path = REPO_ROOT / relative
        if path.is_file():
            referenced.update(PATH_PATTERN.findall(path.read_text(encoding="utf-8")))
    missing_refs = sorted(item for item in referenced if not (REPO_ROOT / item).exists())
    check(not missing_refs, "referenced repository paths exist" + (f": {missing_refs}" if missing_refs else ""))

    pdfs = [
        path
        for path in REPO_ROOT.rglob("*.pdf")
        if ".git" not in path.parts and "output" not in path.parts and ".venv" not in path.parts
    ]
    check(
        pdfs == [REPO_ROOT / "reference" / "Karina_Rohra_Digital_Marketing_Resume_FINAL.pdf"],
        "final resume is the only PDF in the repository",
    )

    try:
        environment = json.loads(read(".cursor/environment.json"))
        install = environment.get("install", "")
        environment_ok = (
            "python3-venv" in install
            and "python3 -m venv .venv" in install
            and ".venv/bin/python -m pip install" in install
            and "requirements.txt" in install
            and "scripts/build_resume_pdf.py" in install
            and "scripts/validate_config.py" in install
        )
    except (json.JSONDecodeError, OSError):
        environment_ok = False
    check(environment_ok, "cloud environment install covers PDF dependencies and validation")

    requirements = read("requirements.txt") if (REPO_ROOT / "requirements.txt").is_file() else ""
    check("reportlab==" in requirements and "pypdf==" in requirements, "PDF Python dependencies are pinned")

    syntax_ok = True
    for relative in ("scripts/build_resume_pdf.py", "scripts/validate_config.py"):
        try:
            py_compile.compile(str(REPO_ROOT / relative), doraise=True)
        except py_compile.PyCompileError:
            syntax_ok = False
    check(syntax_ok, "Python files are syntactically valid")

    schema_ok = False
    try:
        schema = json.loads(read("scripts/resume_schema.json"))
        schema_ok = schema.get("properties", {}).get("candidate_name", {}).get("const") == "Karina Rohra"
    except json.JSONDecodeError:
        schema_ok = False
    check(schema_ok, "resume schema requires the candidate name")

    secret_hits: list[str] = []
    for path in REPO_ROOT.rglob("*"):
        if not path.is_file() or path.suffix.lower() not in TEXT_SUFFIXES:
            continue
        if ".git" in path.parts or "output" in path.parts or ".venv" in path.parts:
            continue
        if SECRET_PATTERN.search(path.read_text(encoding="utf-8", errors="ignore")):
            secret_hits.append(str(path.relative_to(REPO_ROOT)))
    check(not secret_hits, "no secret assignments are committed" + (f": {secret_hits}" if secret_hits else ""))

    pdf_ok = False
    pdf_detail = ""
    try:
        from pypdf import PdfReader

        master = REPO_ROOT / "reference" / "Karina_Rohra_Digital_Marketing_Resume_FINAL.pdf"
        reader = PdfReader(str(master))
        text = "\n".join((page.extract_text() or "") for page in reader.pages)
        folded = re.sub(r"\s+", " ", text).casefold()
        pdf_ok = len(reader.pages) >= 1 and "karina rohra" in folded and "ofcoursesocial" in folded
        if not pdf_ok:
            pdf_detail = "master PDF text did not contain the candidate name and verified employer"
    except Exception as exc:
        pdf_detail = str(exc)
    check(pdf_ok, "master PDF opens and contains the candidate name and verified content" + (f" ({pdf_detail})" if pdf_detail else ""))

    self_test = subprocess.run(
        [sys.executable, str(REPO_ROOT / "scripts" / "build_resume_pdf.py"), "--self-test"],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    check(
        self_test.returncode == 0,
        "PDF builder self-test generates and validates a real PDF"
        + (f" ({self_test.stderr.strip()})" if self_test.returncode else ""),
    )

    incomplete_files = []
    for relative in (
        "config/job_preferences.md",
        "config/answer_bank.md",
        "config/target_config_block.md",
        "config/runtime.md",
    ):
        text = read(relative) if (REPO_ROOT / relative).is_file() else ""
        if any(marker in text for marker in ("TODO", "NOT CONFIGURED", "NOT_CONFIGURED")):
            incomplete_files.append(relative)
    if mode == "LIVE":
        check(
            not incomplete_files,
            "LIVE mode has no TODO or unconfigured required fields"
            + (f": {incomplete_files}" if incomplete_files else ""),
        )
    elif incomplete_files:
        print(
            "NOTE  REVIEW_ONLY is allowing incomplete user fields: "
            + ", ".join(incomplete_files)
        )

    print("")
    if failures:
        print(f"{len(failures)} check(s) failed")
        return 1
    print("configuration validation passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
