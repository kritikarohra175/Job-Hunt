from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
required = [
    ROOT / "config/master_profile.md",
    ROOT / "config/job_preferences.md",
    ROOT / "config/application_rules.md",
    ROOT / "config/job_scoring.md",
    ROOT / "config/resume_tailoring.md",
    ROOT / "config/answer_bank.md",
    ROOT / "config/red_flags.md",
    ROOT / "config/site_policy.md",
    ROOT / "config/runtime.md",
]
missing = [str(p) for p in required if not p.exists()]
if missing:
    print("MISSING_FILES")
    print("\n".join(missing))
    sys.exit(2)

text = "\n".join(p.read_text(encoding="utf-8") for p in required)
for marker in ("TODO", "NOT CONFIGURED"):
    if marker in text:
        print(f"CONFIG_INCOMPLETE: {marker}")
        # Do not fail for review mode; fail only when LIVE.
        if "RUN_MODE=LIVE" in (ROOT / "config/runtime.md").read_text(encoding="utf-8"):
            sys.exit(3)

print("CONFIG_OK")
