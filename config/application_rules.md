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
- An India role whose stated monthly INR salary range is entirely below ₹20,000/month.
- A night shift or rotational shift that is not fully remote.
- A schedule that requires more than 5 workdays per week.
- Suspicious or unverifiable employers where risk is material.
- Applications asking the candidate to create fraudulent documents or misrepresent experience.

## Duplicate handling

Google Sheets is the authoritative application history. `data/application_tracker.csv` is a backup cache only.

Check both the Google Sheet and the CSV before treating a job as new. A match in either source is a duplicate. The Sheet remains authoritative when it can be read. The CSV check does not replace the Sheet.

Treat these as duplicates when they resolve to the same opportunity in either source:

- Same canonical job URL.
- Same company + normalized title + substantially same job description.
- Same external ATS posting duplicated across boards.

A GitHub commit of the CSV is not sufficient deduplication. If the Sheet cannot be read, still check the CSV, mark deduplication incomplete, and do not submit.

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

A LinkedIn or Naukri listing that cannot be fully accessed or safely automated is the exception in the next section. Do not mark that listing `Blocked - Review` and do not reject it for the access or automation limit.

## LinkedIn and Naukri — Manual Apply

Use this path only for LinkedIn and Naukri. It does not change scoring, eligibility, salary, experience, location, hard-stop actions, volume caps, or `RUN_MODE`.

A listing is on this path when the source is LinkedIn or Naukri and any of the following is true:

- The full listing or application cannot be accessed.
- Completing it would require login or stored credentials, cookies, tokens, or passwords.
- Completing it would require bypassing CAPTCHA, MFA, an anti-bot system, an identity check, or an access restriction.
- The platform disallows automated application, or the normal Apply flow cannot be finished safely.

When that is true:

1. Do not reject the listing because of that access or automation limit.
2. Do not log in with stored credentials, cookies, tokens, or passwords.
3. Do not bypass CAPTCHA, MFA, anti-bot systems, identity checks, or access restrictions.
4. Do not click a final Submit or Apply control on LinkedIn or Naukri. This is true in both `REVIEW_ONLY` and `LIVE`.
5. Keep evaluating when enough information is already available. Apply the existing filters and `config/job_scoring.md` to that information. Do not adjust the score because the status will be Manual Apply.
6. If those existing rules reject the role, reject it. Record the eligibility reason. Do not relabel an eligibility rejection as Manual Apply.
7. If the role passes the existing filters and scores 70 or above, including a role that existing rules would prepare or send to review, set `application_status` to `Manual Apply`. Put every existing review reason in the hold reason. A 70–84 score, a salary overlap, or an unresolved non-rejecting field stays that kind of review inside the hold reason. It does not become a rejection, and it does not become a LIVE submission.
8. If the public information is not enough to apply a mandatory filter or to score honestly, do not invent the missing facts and do not reject the listing for the access limit. Set `application_status` to `Manual Apply`, leave `match_score` blank, and set the hold reason to the missing facts.
9. When the role is eligible under step 7, generate and validate the tailored resume PDF. That packet counts toward `MAX_APPLICATIONS_PER_RUN`. After the cap is reached, stop creating new packets, keep logging further Manual Apply rows, and state in the hold reason that the resume was not generated because the per-run cap was reached.
10. For a role on step 7, prepare only non-sensitive answers that already exist in `config/answer_bank.md`. Copy those approved answers into `screening_questions` and into `output/manual_apply/<Company>_<Role>_answers.md`. Do not answer a hard-stop question that the answer bank does not answer exactly. Leave that field blank and name it in the hold reason.

Content hard stops in `config/red_flags.md` still stop the answer. Do not guess, bypass, or submit. On LinkedIn and Naukri, a visible content hard stop stays `Blocked - Review`. Access and automation barriers on those two platforms use `Manual Apply` instead.

Record every Manual Apply row with:

- job URL in `job_url`
- company
- role in `job_title`
- location
- score in `match_score` when it can be scored without inventing facts
- deadline in `application_deadline` when the posting states one, and the same date in `notes`
- stated salary information in `salary_range`; leave it blank when salary is not stated
- rejection or hold reason in `rejection_reason`
- source as `LinkedIn` or `Naukri`

Also set `application_method` to `Manual`. Leave `date_applied`, `confirmation_id`, and `confirmation_url` empty. A Manual Apply row is not a submission.

If the same job is already in the tracker, update that row instead of adding a duplicate.
