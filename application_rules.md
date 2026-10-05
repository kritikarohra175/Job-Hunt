# Application Rules

## Operating mode

Read `config/runtime.md` first.
- RUN_MODE=REVIEW_ONLY: NEVER submit or click a final Apply/Submit button. Prepare everything up to the final step.
- RUN_MODE=LIVE: routine applications may be submitted only when every rule below is satisfied.

## Auto-apply threshold

Default score: 85/100. A score never overrides a hard stop.

## Mandatory preconditions for LIVE submission
1. Role, experience, location, work arrangement, salary, and quality filters pass.
2. Score >= configured threshold.
3. Exact opportunity has not previously been applied to.
4. Tailored PDF resume exists and has been validated.
5. All factual fields are verified.
6. No sensitive/legal/authorization question requires guessing.
7. No CAPTCHA, MFA/2FA, identity check, payment, or anti-bot barrier must be bypassed.
8. Site/workflow permits the automation.
9. Normal job application flow only.

## Resume
The master resume is the only factual source. Tailor before applying. Never overwrite the master.
A markdown/HTML/text draft is NOT an acceptable application attachment. A real PDF must exist at submission time.
Filename: `Karina_Rohra_<Company>_<Role>.pdf`.

## Questions
Allowed: identity, verified education/employment facts, and approved answers in `config/answer_bank.md`.
Stop for work authorization, sponsorship, criminal history, medical/disability, demographic questions, legal declarations, unconfigured salary, or any unknown factual question.

## Duplicates
Deduplicate by canonical URL; then company + normalized title + substantially same JD. Treat cross-board duplicates as one opportunity.

## Disqualifiers
Reject: sales/telecalling/field sales disguised as marketing, commission-only, MLM/network marketing, candidate-paid roles, unpaid roles unless explicitly enabled, senior roles, >2 years clearly required, suspicious employers, fraudulent-document requests.

## Volume
Respect `config/runtime.md` limits.
