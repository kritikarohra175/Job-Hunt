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
- the headline or summary names the exact target job title from `tailoring.role`
- plain punctuation; avoid symbols, emoji, or decorative characters that an ATS may not map to text

## PDF workflow

Tailor only from verified candidate facts. Do not use an older resume as source material.

1. Produce a structured resume that validates against `scripts/resume_schema.json`.
2. Generate a real PDF with `scripts/build_resume_pdf.py`.
3. The builder validates the PDF visually and in its machine-readable text layer before it is written to the destination (see below).
4. Attach only that PDF. Never attach Markdown, TXT, or JSON as the resume.
5. Never overwrite `reference/Karina_Rohra_Digital_Marketing_Resume_FINAL.pdf`.
6. Save the tailored file under `output/resumes/` with a name such as `Karina_Rohra_<Company>_<Role>.pdf`.

The structured JSON is an input to the PDF builder. It is not a resume and must not be uploaded.

## Visual and machine-readable validation

A tailored resume must be readable by a normal human AND cleanly extractable by an ATS. Every tailored PDF must pass both checks before it is used for an application or Manual Apply opportunity, uploaded, or stored in the Tailored Resumes Google Drive folder.

After generating each PDF, `scripts/build_resume_pdf.py`:

1. Confirms the PDF opens, is not encrypted, and has at least one page with extractable text.
2. Extracts the text with the existing PDF parser (pypdf).
3. Runs an independent text-extraction pass (pypdf layout engine) and audits every font for a Unicode mapping (`/ToUnicode` or a standard text encoding; no Type3 or symbolic fonts).
4. Verifies that the expected text is extracted correctly: `Karina Rohra`, the target job title, `Digital Marketing`, the relevant Social Media / SEO / Content Marketing keywords, every employer and job title, every education entry, every certification, and every tailored sentence.
5. Detects character-encoding corruption: replacement characters, control characters, private-use or format characters, mojibake, `(cid:N)` markers, malformed words, broken word spacing, and characters outside the ATS-safe set.
6. Rejects the PDF if text that looks right visually is corrupted or unreadable in the text layer, or if an important ATS keyword is missing.
7. On rejection, regenerates the PDF with the ATS-safe profile (standard Helvetica, strict ASCII text with the same meaning) and validates it again.
8. Deletes any PDF that fails. Do not upload or store a failed PDF. Only a PDF that passes both checks reaches its destination path.

Run `.venv/bin/python scripts/build_resume_pdf.py --validate <pdf> --require-text "<Role>"` to re-check any existing PDF, and add `--report <path>.json` to keep the check result as evidence. Record the validation result in the daily report.

## Final validation

Before submission, confirm:
- No invented facts.
- No conflicting dates.
- No unverified tools.
- No inflated metrics.
- No role inflation.
- JD keywords are represented where legitimately supported.
- The resume is concise and targeted.
- The attached file is a validated PDF that passed both the visual and the machine-readable check.
- The master resume file is unchanged.
