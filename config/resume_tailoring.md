# Resume Tailoring Rules

## Objective

Create the strongest truthful one- or two-page ATS-friendly resume for the exact job.

## Process

1. Read the full JD.
2. Extract responsibilities, must-have skills, nice-to-have skills, tools, channel names, industry terms, seniority signals, and recurring keywords.
3. Map those requirements to verified candidate evidence in `config/master_profile.md` and `reference/Karina_Rohra_Digital_Marketing_Resume_FINAL.pdf`.
4. Identify unsupported requirements. Never fabricate them.
5. Rewrite the professional summary to match the role while staying truthful.
6. Reorder and rename skills only when truthful and ATS-helpful.
7. Select and prioritize the most relevant experience bullets.
8. Rephrase bullets for clarity, ownership, and relevance without changing factual meaning.
9. Keep dates, employers, education, certifications, and job titles consistent with the source resume.
10. Run a final contradiction/fabrication check.

## Keyword rules

- Mirror exact JD terminology where it truthfully maps to existing skills.
- Prefer natural keyword placement over keyword stuffing.
- Do not repeat the same keyword unnaturally.
- Do not claim an advanced level for a basic skill.
- Do not add a tool because it is mentioned in the JD unless it is verified in the profile.

## Summary rules

The summary should answer:
- What level is the candidate?
- What digital marketing areas are relevant?
- What evidence supports the fit?
- What is the candidate currently studying?

Avoid generic personality filler.

## Experience rules

For recruitment roles, emphasize only transferable skills that are directly relevant to the JD, such as:
- audience-specific communication
- LinkedIn outreach
- research
- stakeholder coordination
- follow-up
- deadline management
- written communication

Do not rewrite recruitment experience as marketing experience.

## Project/practice rules

Use the verified social media/content practice section when it strengthens relevance. Do not convert practice into paid employment.

## Format rules

Prefer:
- standard headings
- simple typography
- no tables in the resume body
- no text boxes
- no icons used as critical data carriers
- consistent dates
- ATS-readable contact details

## PDF workflow

Tailor only from verified candidate facts. Do not use an older resume as source material.

1. Produce a structured resume that validates against `scripts/resume_schema.json`.
2. Generate a real PDF with `scripts/build_resume_pdf.py`.
3. Validate that the PDF opens and that its extracted text contains the candidate name and the tailored summary.
4. Attach only that PDF. Never attach Markdown, TXT, or JSON as the resume.
5. Never overwrite `reference/Karina_Rohra_Digital_Marketing_Resume_FINAL.pdf`.
6. Save the tailored file under `output/resumes/` with a name such as `Karina_Rohra_<Company>_<Role>.pdf`.

The structured JSON is an input to the PDF builder. It is not a resume and must not be uploaded.

## Final validation

Before submission, confirm:
- No invented facts.
- No conflicting dates.
- No unverified tools.
- No inflated metrics.
- No role inflation.
- JD keywords are represented where legitimately supported.
- The resume is concise and targeted.
- The attached file is a validated PDF.
- The master resume file is unchanged.
