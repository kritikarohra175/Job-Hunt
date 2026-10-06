# Job Scoring

Score every candidate opportunity from 0 to 100 before tailoring a resume.

## Weights

Role relevance: 25
Experience fit: 20
Verified skill match: 20
Location/work arrangement fit: 10
Salary fit: 10
Company/industry preference fit: 5
JD quality/clarity: 5
Application feasibility: 5

## Definitions

### Role relevance (25)
25 = directly in digital marketing/social media/content/SEO and aligned with target titles.
15–24 = closely related marketing role with a strong digital component.
5–14 = mixed/ambiguous role.
0–4 = mostly unrelated.

### Experience fit (20)
20 = 0 years/fresher/internship explicitly accepted.
16 = 0–1 year.
10 = 1–2 years but clearly junior/flexible.
0–5 = >2 years required.

### Verified skill match (20)
Compare only against verified profile skills. Penalize requirements for tools/skills that are absent or materially more advanced than the profile.

### Location/work arrangement (10)
Use `config/job_preferences.md`. If not configured, mark this component `UNRESOLVED` and route to review instead of inventing fit.

### Salary fit (10)
Use the stated range and the India monthly floor in `config/job_preferences.md`. Never invent a salary or convert another currency into INR.

An India role whose entire stated monthly INR range is below ₹20,000/month is a rejection before scoring. A range that overlaps ₹20,000/month is review, with salary fit below 10. A range that starts at or above ₹20,000/month can receive full salary fit when the rest of the role passes. Undisclosed salary does not by itself fail this component.

### Company/industry fit (5)
Reward legitimate employers, relevant industries, and clear role ownership. Penalize suspicious or irrelevant listings.

### JD quality (5)
Reward clear responsibilities, realistic requirements, named employer, consistent location, and a normal application flow.

### Application feasibility (5)
5 = normal application, no unusual barriers.
3 = slightly complex ATS/form.
1 = highly manual/ambiguous.
0 = blocked/prohibited/suspicious.

## Decision

The numeric threshold is `AUTO_APPLY_THRESHOLD=85` in `config/runtime.md`.

85–100: eligible for LIVE submission only when every application rule and hard stop is clear.
70–84: prepare and record as review.
Below 70: reject.

In `RUN_MODE=REVIEW_ONLY`, a score of 85–100 authorizes preparation only. It does not authorize submission.

A score never overrides a hard-stop rule or `RUN_MODE`.
