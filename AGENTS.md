# Project Instructions: Job Application Agent

This repository controls a job-search/application workflow. Follow these instructions on every run.

## Source of truth

Use `config/master_profile.md` for verified candidate facts.
Use `config/job_preferences.md` for job-search constraints.
Use `config/application_rules.md` for application behavior.
Use `config/job_scoring.md` for scoring.
Use `config/resume_tailoring.md` for resume tailoring.
Use `config/answer_bank.md` for approved recurring answers.
Use `config/red_flags.md` for disqualifiers and stop conditions.
Use `config/site_policy.md` for browser/site safety.

## Non-negotiable truthfulness rule

Never invent employment, experience, metrics, clients, revenue, certifications, tools, degrees, responsibilities, results, dates, job titles, portfolio work, or qualifications. Never turn weak familiarity into professional experience. Never answer a factual application question by guessing.

## Safety and authorization

Do not bypass CAPTCHA, MFA/2FA, identity checks, anti-bot measures, paywalls, access controls, or site restrictions. Do not scrape or automate a site in a way that violates its terms or access rules. If automation is prohibited or blocked, record the reason and stop that application.

## Application behavior

Prefer quality over volume. Deduplicate jobs. Tailor the resume before applying. Do not submit an application until the final resume has been generated and the application fields have been sanity-checked.

Stop rather than guess when a question requires legal, work-authorization, sponsorship, demographic, medical, criminal-history, disability, or other sensitive information.

Do not send recruiter outreach messages unless explicitly enabled in the configuration.

## Files

Generated artifacts should be stored under `output/` in the automation workspace or in the configured Google Drive folders. Do not overwrite the master resume.
