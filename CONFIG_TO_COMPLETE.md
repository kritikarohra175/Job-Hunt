# One-time values you must fill before LIVE mode

Approved candidate preferences are now set in `config/job_preferences.md`, `config/answer_bank.md`, and `config/target_config_block.md`.

Configured:
- TARGET_LOCATIONS
- ACCEPT_REMOTE
- ACCEPT_HYBRID
- ACCEPT_ONSITE
- OPEN_TO_RELOCATION
- OPEN_TO_INTERNATIONAL_RELOCATION
- ACCEPTED_COUNTRIES
- ACCEPTED_CITIES
- MIN_MONTHLY_SALARY_INR
- PREFERRED_MONTHLY_SALARY_INR
- INTERNATIONAL_SALARY_RULE
- PREFERRED_SHIFTS
- MAX_WORKDAYS_PER_WEEK
- ACCEPT_NIGHT_SHIFTS
- ACCEPT_ROTATIONAL_SHIFTS
- Salary expectation for India and international roles
- Work authorization for India and international roles
- Visa sponsorship
- Relocation
- Availability: Immediately

Still missing:
- `SPREADSHEET_ID`

Paste the real Google Sheet ID in `config/runtime.md` on the line `SPREADSHEET_ID=NOT_CONFIGURED`, replacing `NOT_CONFIGURED`. Then set the same value on `SPREADSHEET_ID=` in `config/target_config_block.md`. Do not invent an ID.

`RUN_MODE` stays `REVIEW_ONLY` in `config/runtime.md`. Do not submit applications in that mode.
