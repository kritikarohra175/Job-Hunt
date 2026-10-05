# Resume Tailoring Rules

1. Read the full JD.
2. Extract responsibilities, must-have skills, nice-to-have skills, tools, channels, industry terms and recurring keywords.
3. Map each relevant requirement to verified evidence in `config/master_profile.md`.
4. Rewrite the summary and relevant bullets without changing factual meaning.
5. Reorder skills only when truthful.
6. Keep employer names, titles, dates, education and certifications exact.
7. Never add a skill/tool/achievement because it appears in the JD unless verified in the master profile.
8. Never turn practice, exposure or support into professional ownership.
9. Generate a structured JSON resume using `scripts/resume_schema.json`.
10. Generate a REAL PDF using `scripts/build_resume_pdf.py`.
11. Validate that the PDF exists, is non-empty, opens successfully, and contains the candidate's name and the tailored role-relevant content.
12. The final application may attach ONLY the validated PDF, never markdown or a text draft.

ATS rules: standard headings, simple typography, no tables/text boxes/icons as critical data carriers, natural keyword use, concise 1–2 pages.
