# Application Rules

## Operating mode

Operating mode: REVIEW ONLY.

During REVIEW ONLY mode:
- Never submit an application.
- Never click a final Submit / Apply button.
- Perform job discovery, filtering, scoring, resume tailoring, and form preparation.
- Record what would have been submitted in the tracker.
- Stop immediately before final submission.

The agent may submit a routine application only when all of the following are true:

1. The job passes role, experience, location, work arrangement, salary, and quality filters.
2. The job score meets the auto-apply threshold.
3. The exact job has not previously been applied to.
4. The tailored resume has been created and validated.
5. No factual uncertainty remains in the application fields.
6. No sensitive/legal/authorization question requires guessing.
7. No CAPTCHA, MFA/2FA, identity check, payment, or anti-bot barrier must be bypassed.
8. The site/workflow permits the agent's automated interaction.
9. The final submission is a normal job application, not a contract, paid service, or unrelated sales funnel.

## Auto-apply threshold

Default auto-apply score: 85/100.

70–84: may be prepared and recorded as REVIEW unless the workflow is explicitly configured to allow broader auto-apply.
Below 70: reject.

## What must be rejected

- Sales/telecalling/field sales roles disguised as marketing.
- Commission-only roles.
- Jobs requiring payment or purchase from candidates.
- MLM/network-marketing/business-opportunity schemes.
- Unpaid roles unless explicitly configured otherwise.
- Roles primarily unrelated to digital marketing.
- Senior/manager roles.
- Clearly >2 years experience requirements.
- Suspicious or unverifiable employers where risk is material.
- Applications asking the candidate to create fraudulent documents or misrepresent experience.

## Duplicate handling

Treat these as duplicates when they resolve to the same opportunity:
- Same canonical job URL.
- Same company + normalized title + substantially same JD.
- Same external ATS posting duplicated across boards.

Never submit the same job twice.

## Resume rule

The resume is tailored for the job before application submission.
Never overwrite the master resume.
Each tailored resume must receive a stable filename such as:
`Karina_Rohra_<Company>_<Role>.pdf`

## Application questions

Allowed automatic questions:
- Name
- Email
- Phone
- LinkedIn URL
- Education dates
- Employment dates/titles from master profile
- Skills explicitly verified in master profile
- Availability only when an approved answer exists

Hard-stop questions unless an exact answer exists in `config/answer_bank.md`:
- Work authorization
- Visa sponsorship
- Criminal history
- Medical/disability information
- Demographic/equal-opportunity questions
- Salary expectation if not configured
- Non-compete / legal declarations
- Security checks
- Anything that asks the agent to certify facts not present in the profile

## Cover letters

Generate a cover letter only when:
- the employer explicitly requests one; or
- a tailored letter materially improves the application and the job score is 90+.

Do not create generic filler.

## Confirmation evidence

After submission, capture the confirmation URL, confirmation message, application ID, or equivalent evidence when available.
Record date/time in the tracker.

## Failure handling

If a form breaks, a field is ambiguous, or automation is blocked:
- Do not guess.
- Do not bypass the control.
- Save the job URL and the failure reason.
- Mark status `Blocked - Review`.
