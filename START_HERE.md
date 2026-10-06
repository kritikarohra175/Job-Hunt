# START HERE

The canonical files are under `config/`, `prompts/`, `scripts/`, `data/`, `reference/`, and `.cursor/`. Do not create a second copy of those files at the repository root.

`config/runtime.md` is `RUN_MODE=REVIEW_ONLY`. That mode never submits an application.

Approved locations, salary rules, schedule, work authorization, and answers are in:

- `config/job_preferences.md`
- `config/answer_bank.md`
- `config/target_config_block.md`

The only authoritative resume is `reference/Karina_Rohra_Digital_Marketing_Resume_FINAL.pdf`.

The application tracker ID, tab, and Drive resume file ID are in `config/runtime.md`. Google Sheets is the authority. `data/application_tracker.csv` is a backup cache.

The daily run instructions are `prompts/daily_automation_prompt.md`.

LinkedIn and Naukri listings that cannot be fully accessed or safely automated stay in the report as `Manual Apply` when the existing eligibility rules do not reject them. Open the job URL and finish those applications. The run does not log in and does not click Submit or Apply on those platforms.
