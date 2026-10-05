# Application Rules

## Operating mode

The only mode switch is `config/runtime.md`.

RUN_MODE=REVIEW_ONLY

During `REVIEW_ONLY`:

- Never submit an application.
- Never click a final Submit or Apply button.
- Discovery, filtering, scoring, resume tailoring, and form preparation are allowed.
- Record what would have been submitted in the tracker with a review-only status.
- Stop immediately before final submission.

`LIVE` may submit a routine application only when all of the following are true:

1. `RUN_MODE=LIVE` is set in `config/runtime.md` by an explicit user edit.
2. The job passes role, experience, location, work arrangement, salary, and quality filters.
3. The job score is at least `AUTO_APPLY_THRESHOLD=85`.
4. The exact job has not previously been applied to, based on the Google Sheet tracker.
5. The tailored resume PDF has been created and validated.
6. No factual uncertainty remains in the application fields.
7. No sensitive, legal, or authorization question requires guessing.
8. No CAPTCHA, MFA/2FA, identity check, payment, or anti-bot barrier must be bypassed.
9. The site workflow permits automated interaction.
10. The final submission is a normal job application, not a contract, paid service, or unrelated sales funnel.
11. The run is still inside `MAX_APPLICATIONS_PER_RUN=5` and `MAX_APPLICATIONS_PER_DAY=10`.

A passing score does not override `REVIEW_ONLY`.

## Auto-apply threshold

AUTO_APPLY_THRESHOLD=85

70–84: prepare and record as review.
Below 70: reject.

## What must be rejected

- Sales, telecalling, or field sales roles disguised as marketing.
- Commission-only roles.
- Jobs requiring payment or purchase from candidates.
- MLM, network-marketing, or business-opportunity schemes.
- Unpaid roles unless explicitly configured otherwise.
- Roles primarily unrelated to digital marketing.
- Senior or manager roles.
- Clearly more than 2 years of required experience.
- Suspicious or unverifiable employers where risk is material.
- Applications asking the candidate to create fraudulent documents or misrepresent experience.

## Duplicate handling

Google Sheets is the authoritative application history. `data/application_tracker.csv` is a backup cache only.

Deduplication must check both the Google Sheet and the local CSV. A listing that matches either source is a duplicate. The Sheet remains authoritative when it can be read. The CSV check does not replace the Sheet.

Treat these as duplicates when they resolve to the same opportunity:

- Same canonical job URL.
- Same company + normalized title + substantially same job description.
- Same external ATS posting duplicated across boards.

Read the Google Sheet and `data/application_tracker.csv` before deciding that a job is new. A GitHub commit of the CSV is not sufficient deduplication. If the Sheet cannot be read, still check the local CSV, mark deduplication incomplete, and do not submit.

Never submit the same job twice.

## Resume rule

Tailor only from `config/master_profile.md` and `reference/Karina_Rohra_Digital_Marketing_Resume_FINAL.pdf`.
Do not use any older resume version.

Generate a structured resume, then a real PDF, then validate that PDF before it is attached.
Never attach Markdown, TXT, or JSON as the resume.
Never overwrite the master resume.

Each tailored resume must be a PDF with a stable filename such as:

`Karina_Rohra_<Company>_<Role>.pdf`

## Application questions

Allowed automatic questions:

- Name
- Email
- Phone
- LinkedIn URL
- Education dates
- Employment dates and titles from the master profile
- Skills explicitly verified in the master profile
- Availability only when an approved answer exists

Hard-stop questions unless an exact answer exists in `config/answer_bank.md`:

- Work authorization
- Visa sponsorship
- Criminal history
- Medical or disability information
- Demographic or equal-opportunity questions
- Salary expectation if not configured
- Relocation if not configured
- Non-compete or legal declarations
- Security checks
- Anything that asks the agent to certify facts not present in the profile

## Cover letters

Generate a cover letter only when:

- the employer explicitly requests one; or
- a tailored letter materially improves the application and the job score is 90+.

Do not create generic filler. Do not invent facts in a cover letter.

## Confirmation evidence

After a LIVE submission, capture the confirmation URL, confirmation message, application ID, or equivalent evidence when available.
Record date and time in the tracker.
In `REVIEW_ONLY`, do not create a fake confirmation. Record the status as prepared and not submitted.

## Failure handling

If a form breaks, a field is ambiguous, or automation is blocked:

- Do not guess.
- Do not bypass the control.
- Save the job URL and the failure reason.
- Mark status `Blocked - Review`.
