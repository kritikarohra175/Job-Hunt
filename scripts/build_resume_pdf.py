#!/usr/bin/env python3
"""Build a truthful tailored resume PDF from structured JSON.

The JSON file is builder input only. Never attach JSON, Markdown, or TXT
as the resume. This script refuses to overwrite the master resume.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
import tempfile
from pathlib import Path
from xml.sax.saxutils import escape

REPO_ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = Path(__file__).resolve().parent / "resume_schema.json"
PROFILE_PATH = REPO_ROOT / "config" / "master_profile.md"
MASTER_RESUME = REPO_ROOT / "reference" / "Karina_Rohra_Digital_Marketing_Resume_FINAL.pdf"
CANDIDATE_NAME = "Karina Rohra"

EXPERIENCE = (
    {
        "title": "Digital Marketing Intern",
        "organization": "Ofcoursesocial",
        "location": "Vadodara, Gujarat, India",
        "dates": "May 2022 - July 2022",
    },
    {
        "title": "Technical Recruiter",
        "organization": "Delta System & Software, Inc.",
        "location": "Vadodara, Gujarat, India",
        "dates": "Oct 2023 - April 2024",
    },
    {
        "title": "Corporate Recruiter",
        "organization": "Analytical Technologies Limited",
        "location": "Vadodara, Gujarat, India",
        "dates": "May 2024 - July 2024",
    },
    {
        "title": "Executive",
        "organization": "K C Mehta & Co LLP",
        "location": "Vadodara, Gujarat, India",
        "dates": "Jan 2025 - June 2025",
    },
)

EDUCATION = (
    {
        "credential": "Master of Business Administration - Digital Marketing",
        "institution": "Dr. D Y Patil Vidyapeeth - Centre for Online Learning",
        "dates": "Jan 2026 - Mar 2028",
    },
    {
        "credential": "Bachelor of Business Administration - Marketing-Relevant Business Degree",
        "institution": "The Maharaja Sayajirao University of Baroda",
        "dates": "Nov 2020 - May 2023",
    },
)

EDUCATION_NOTES = {
    "Currently pursuing",
    "Relevant foundation: marketing concepts, business communication, management, business operations, research, and organizational coordination.",
}

CERTIFICATIONS = {
    "Digital Marketing Certification - HubSpot Academy",
    "SEO Essentials - Semrush Academy",
    "AI Fluency - Anthropic Academy",
    "Claude 101 - Anthropic Academy",
    "US Market & B2B Communication Training - HTD Resources Pvt Ltd",
}

SKILLS = {
    "Digital Marketing": {
        "Campaign Support",
        "Brand Awareness",
        "Lead Generation",
        "Online Marketing",
    },
    "Social Media": {
        "Instagram",
        "LinkedIn",
        "Facebook",
        "Content Planning",
        "Captions",
        "Content Scheduling",
    },
    "Content Marketing": {
        "Blog Writing",
        "Social Media Posts",
        "Landing Page Copy",
        "Email Content",
        "Marketing Copy",
    },
    "SEO": {
        "Keyword Research",
        "On-Page SEO",
        "Meta Descriptions",
        "Title Tags",
        "Headings",
        "Content Optimization",
    },
    "Email Marketing": {
        "Newsletter Content",
        "Email Copy",
        "Campaign Support",
        "List Management Basics",
    },
    "Analytics & Reporting": {
        "Campaign Reports",
        "Engagement Tracking",
        "Traffic Reports",
        "Performance Insights",
    },
    "Research": {
        "Market Research",
        "Competitor Analysis",
        "Audience Research",
        "Content Gap Analysis",
    },
    "Creative Tools": {
        "Canva",
        "PowerPoint",
        "AI-Assisted Content Tools",
        "Basic Creative Direction",
    },
    "Marketing Operations": {
        "Content Calendars",
        "Marketing Materials",
        "Presentations",
        "Digital Asset Organization",
    },
    "Professional Skills": {
        "Communication",
        "Coordination",
        "Time Management",
        "Attention to Detail",
        "Problem Solving",
    },
    "Tools": {
        "Canva",
        "Instagram",
        "LinkedIn",
        "Facebook",
        "MS Excel",
        "PowerPoint",
        "Google Workspace",
        "ChatGPT",
        "Claude",
        "Gemini",
        "AI Content Tools",
    },
}

PORTFOLIO_ITEMS = {
    "Social media captions",
    "Blog and landing page copy",
    "Email content samples",
    "Content calendar samples",
    "Campaign ideas",
    "AI-assisted marketing content and visual concepts",
}

LINKEDIN_PATH = "linkedin.com/in/karinarohra-485282214"

BANNED_PATTERNS = (
    re.compile(r"\d+(?:\.\d+)?\s*%"),
    re.compile(r"[$₹€£]\s*\d"),
    re.compile(r"\b(?:roas|ctr|cpc|cpm|roi)\b", re.IGNORECASE),
    re.compile(
        r"\b(?:google ads|meta ads|facebook ads|instagram ads|linkedin ads)\b",
        re.IGNORECASE,
    ),
    re.compile(
        r"\b(?:increased|grew|boosted|generated|improved)\b[^.%\n]{0,40}\d",
        re.IGNORECASE,
    ),
    re.compile(
        r"\b(?:advanced seo|advanced analytics|paid media|marketing automation)\b",
        re.IGNORECASE,
    ),
    re.compile(r"\bcrm\b", re.IGNORECASE),
)

SENIORITY_PATTERN = re.compile(
    r"\b(?:senior|manager|director|head of|vice president|\bvp\b)\b",
    re.IGNORECASE,
)


class ResumeBuildError(Exception):
    """A truthful-resume check failed."""


def fail(message: str) -> None:
    raise ResumeBuildError(message)


def normalize_space(value: str) -> str:
    return re.sub(r"\s+", " ", value).strip()


def normalize_linkedin(value: str) -> str:
    text = value.strip().lower()
    text = re.sub(r"^https?://", "", text)
    text = re.sub(r"^www\.", "", text)
    return text.rstrip("/")


def experience_key(item: dict) -> tuple[str, str, str, str]:
    return (item["title"], item["organization"], item["location"], item["dates"])


def education_key(item: dict) -> tuple[str, str, str]:
    return (item["credential"], item["institution"], item["dates"])


def locked_profile_strings() -> list[str]:
    values = [
        CANDIDATE_NAME,
        "karinarohra175@gmail.com",
        "+91 90813 83567",
        "Vadodara, Gujarat, India",
        LINKEDIN_PATH,
    ]
    for item in EXPERIENCE:
        values.extend(item.values())
    for item in EDUCATION:
        values.extend(item.values())
    values.extend(sorted(CERTIFICATIONS))
    values.extend(sorted(EDUCATION_NOTES))
    for items in SKILLS.values():
        values.extend(sorted(items))
    values.extend(sorted(PORTFOLIO_ITEMS))
    return values


def assert_allowlist_matches_profile() -> None:
    if not PROFILE_PATH.is_file():
        fail(f"missing master profile: {PROFILE_PATH}")
    profile = PROFILE_PATH.read_text(encoding="utf-8")
    missing = [value for value in locked_profile_strings() if value not in profile]
    if missing:
        fail("allowlist is not fully present in config/master_profile.md: " + "; ".join(missing))


def load_resume(path: Path) -> dict:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        fail(f"structured resume is not valid JSON: {exc}")
    try:
        import jsonschema
    except ImportError as exc:
        fail(f"jsonschema is not installed ({exc}). Install requirements.txt.")
    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    validator = jsonschema.Draft202012Validator(schema)
    errors = sorted(validator.iter_errors(data), key=lambda item: list(item.path))
    if errors:
        rendered = "; ".join(error.message for error in errors[:8])
        fail(f"structured resume does not match scripts/resume_schema.json: {rendered}")
    return data


def assert_truthful(resume: dict) -> None:
    assert_allowlist_matches_profile()
    if resume["candidate_name"] != CANDIDATE_NAME:
        fail("candidate name does not match the final resume")
    if normalize_linkedin(resume["contact"]["linkedin"]) != LINKEDIN_PATH:
        fail("LinkedIn URL does not match the final resume")
    if SENIORITY_PATTERN.search(resume["headline"]):
        fail("headline adds seniority that is not on the final resume")

    seen_roles = set()
    allowed_roles = {experience_key(item) for item in EXPERIENCE}
    for item in resume["experience"]:
        key = experience_key(item)
        if key not in allowed_roles:
            fail(
                "experience entry is not on the final resume: "
                f"{item['title']} at {item['organization']}"
            )
        if key in seen_roles:
            fail(f"duplicate experience entry: {item['title']}")
        seen_roles.add(key)

    allowed_education = {education_key(item) for item in EDUCATION}
    seen_education = set()
    for item in resume["education"]:
        key = education_key(item)
        if key not in allowed_education:
            fail(f"education entry is not on the final resume: {item['credential']}")
        if key in seen_education:
            fail(f"duplicate education entry: {item['credential']}")
        seen_education.add(key)
        for note in item.get("notes", []):
            if note not in EDUCATION_NOTES:
                fail("education note is not on the final resume")

    unknown_certs = [item for item in resume["certifications"] if item not in CERTIFICATIONS]
    if unknown_certs:
        fail("certification is not on the final resume: " + "; ".join(unknown_certs))

    for group in resume["skill_groups"]:
        allowed_items = SKILLS.get(group["category"])
        if allowed_items is None:
            fail(f"skill category is not on the final resume: {group['category']}")
        unknown_items = [item for item in group["items"] if item not in allowed_items]
        if unknown_items:
            fail("skill is not verified: " + "; ".join(unknown_items))

    unknown_portfolio = [
        item for item in resume.get("portfolio_items", []) if item not in PORTFOLIO_ITEMS
    ]
    if unknown_portfolio:
        fail("portfolio item is not verified: " + "; ".join(unknown_portfolio))

    prose = [resume["headline"], resume["summary"]]
    prose.append(resume["tailoring"].get("emphasis", ""))
    for item in resume["experience"]:
        prose.extend(item["bullets"])
    for item in resume["education"]:
        prose.extend(item.get("notes", []))
    prose.extend(resume.get("ai_assisted_bullets", []))
    for text in prose:
        for pattern in BANNED_PATTERNS:
            if pattern.search(text):
                fail("tailored text introduces an unsupported metric, tool, or claim")


def assert_safe_output(path: Path) -> Path:
    resolved = path.expanduser().resolve()
    master = MASTER_RESUME.resolve()
    if not MASTER_RESUME.is_file():
        fail(f"authoritative resume is missing: {MASTER_RESUME}")
    if resolved == master or resolved.name == master.name:
        fail("refusing to overwrite the master resume")
    if master.parent == resolved.parent:
        fail("refusing to write a resume into reference/")
    if resolved.suffix.lower() != ".pdf":
        fail("resume output must be a PDF. Markdown, TXT, and JSON cannot be the resume.")
    resolved.parent.mkdir(parents=True, exist_ok=True)
    return resolved


def render_pdf(resume: dict, destination: Path) -> None:
    try:
        from reportlab.lib.colors import HexColor
        from reportlab.lib.enums import TA_LEFT
        from reportlab.lib.pagesizes import A4
        from reportlab.lib.styles import ParagraphStyle
        from reportlab.lib.units import inch
        from reportlab.platypus import HRFlowable, Paragraph, SimpleDocTemplate, Spacer
    except ImportError as exc:
        fail(f"reportlab is not installed ({exc}). Install requirements.txt.")

    styles = {
        "name": ParagraphStyle(
            "Name",
            fontName="Times-Bold",
            fontSize=16,
            leading=19,
            alignment=TA_LEFT,
            textColor=HexColor("#1F2933"),
            spaceAfter=2,
        ),
        "headline": ParagraphStyle(
            "Headline",
            fontName="Times-Italic",
            fontSize=10,
            leading=13,
            textColor=HexColor("#334E68"),
            spaceAfter=4,
        ),
        "contact": ParagraphStyle(
            "Contact",
            fontName="Times-Roman",
            fontSize=9,
            leading=12,
            spaceAfter=8,
        ),
        "section": ParagraphStyle(
            "Section",
            fontName="Times-Bold",
            fontSize=11,
            leading=14,
            textColor=HexColor("#1F2933"),
            spaceBefore=8,
            spaceAfter=3,
        ),
        "body": ParagraphStyle(
            "Body",
            fontName="Times-Roman",
            fontSize=10,
            leading=13,
            spaceAfter=4,
        ),
        "role": ParagraphStyle(
            "Role",
            fontName="Times-Bold",
            fontSize=10.5,
            leading=13,
            spaceBefore=4,
            spaceAfter=0,
        ),
        "meta": ParagraphStyle(
            "Meta",
            fontName="Times-Italic",
            fontSize=9.5,
            leading=12,
            spaceAfter=2,
        ),
        "bullet": ParagraphStyle(
            "Bullet",
            fontName="Times-Roman",
            fontSize=10,
            leading=13,
            leftIndent=12,
            bulletIndent=0,
            spaceAfter=1,
        ),
    }

    contact = resume["contact"]
    contact_bits = [
        contact["email"],
        contact["phone"],
        contact["location"],
        contact["linkedin"],
    ]
    if contact.get("availability"):
        contact_bits.append(f"Available: {contact['availability']}")

    story = [
        Paragraph(escape(resume["candidate_name"]), styles["name"]),
        Paragraph(escape(resume["headline"]), styles["headline"]),
        Paragraph(escape(" | ".join(contact_bits)), styles["contact"]),
        HRFlowable(width="100%", thickness=0.6, color=HexColor("#9FB3C8"), spaceAfter=4),
        Paragraph("PROFESSIONAL SUMMARY", styles["section"]),
        Paragraph(escape(resume["summary"]), styles["body"]),
        Paragraph("CORE SKILLS", styles["section"]),
    ]
    for group in resume["skill_groups"]:
        items = ", ".join(group["items"])
        story.append(
            Paragraph(f"<b>{escape(group['category'])}:</b> {escape(items)}", styles["body"])
        )

    story.append(Paragraph("PROFESSIONAL EXPERIENCE", styles["section"]))
    for item in resume["experience"]:
        story.append(Paragraph(escape(item["title"]), styles["role"]))
        story.append(
            Paragraph(
                escape(
                    f"{item['organization']} | {item['location']} | {item['dates']}"
                ),
                styles["meta"],
            )
        )
        for bullet in item["bullets"]:
            story.append(Paragraph(escape(f"• {bullet}"), styles["bullet"]))

    if resume.get("ai_assisted_bullets"):
        story.append(Paragraph("AI-ASSISTED DIGITAL MARKETING EXPERIENCE", styles["section"]))
        for bullet in resume["ai_assisted_bullets"]:
            story.append(Paragraph(escape(f"• {bullet}"), styles["bullet"]))

    story.append(Paragraph("EDUCATION", styles["section"]))
    for item in resume["education"]:
        story.append(Paragraph(escape(item["credential"]), styles["role"]))
        story.append(
            Paragraph(escape(f"{item['institution']} | {item['dates']}"), styles["meta"])
        )
        for note in item.get("notes", []):
            story.append(Paragraph(escape(note), styles["body"]))

    story.append(Paragraph("CERTIFICATIONS & TRAINING", styles["section"]))
    for item in resume["certifications"]:
        story.append(Paragraph(escape(f"• {item}"), styles["bullet"]))

    if resume.get("portfolio_items"):
        story.append(Paragraph("PORTFOLIO", styles["section"]))
        story.append(Paragraph("Portfolio and samples available on request, including:", styles["body"]))
        for item in resume["portfolio_items"]:
            story.append(Paragraph(escape(f"• {item}"), styles["bullet"]))

    document = SimpleDocTemplate(
        str(destination),
        pagesize=A4,
        leftMargin=0.7 * inch,
        rightMargin=0.7 * inch,
        topMargin=0.65 * inch,
        bottomMargin=0.65 * inch,
        title=f"{CANDIDATE_NAME} resume",
        author=CANDIDATE_NAME,
    )
    document.build(story)


def extract_pdf_text(path: Path) -> str:
    header = path.read_bytes()[:5]
    if header != b"%PDF-":
        fail(f"file is not a PDF: {path}")
    try:
        from pypdf import PdfReader
    except ImportError as exc:
        fail(f"pypdf is not installed ({exc}). Install requirements.txt.")
    try:
        reader = PdfReader(str(path))
        if len(reader.pages) < 1:
            fail(f"PDF has no pages: {path}")
        return "\n".join((page.extract_text() or "") for page in reader.pages)
    except ResumeBuildError:
        raise
    except Exception as exc:
        fail(f"PDF could not be opened: {exc}")


def validate_pdf(path: Path, resume: dict | None = None, required_text: list[str] | None = None) -> str:
    text = extract_pdf_text(path)
    folded = normalize_space(text).casefold()
    if "karina rohra" not in folded:
        fail("PDF does not contain the candidate name")
    snippets = list(required_text or [])
    if resume is not None:
        snippets.append(resume["summary"])
        snippets.append(resume["experience"][0]["bullets"][0])
        snippets.append(resume["experience"][0]["organization"])
    for snippet in snippets:
        if normalize_space(snippet).casefold() not in folded:
            fail(f"PDF does not contain required tailored content: {snippet[:80]}")
    return text


def default_output_path(resume: dict) -> Path:
    company = re.sub(r"[^A-Za-z0-9]+", "_", resume["tailoring"]["company"]).strip("_")
    role = re.sub(r"[^A-Za-z0-9]+", "_", resume["tailoring"]["role"]).strip("_")
    company = (company or "Company")[:40]
    role = (role or "Role")[:40]
    return REPO_ROOT / "output" / "resumes" / f"Karina_Rohra_{company}_{role}.pdf"


def build(resume: dict, destination: Path) -> Path:
    assert_truthful(resume)
    output = assert_safe_output(destination)
    master_hash = hashlib.sha256(MASTER_RESUME.read_bytes()).hexdigest()
    render_pdf(resume, output)
    validate_pdf(output, resume)
    if hashlib.sha256(MASTER_RESUME.read_bytes()).hexdigest() != master_hash:
        fail("master resume changed during PDF generation")
    return output


def canonical_test_resume() -> dict:
    return {
        "candidate_name": CANDIDATE_NAME,
        "headline": "Digital Marketing Executive | Social Media | SEO | Content Marketing",
        "contact": {
            "email": "karinarohra175@gmail.com",
            "phone": "+91 90813 83567",
            "location": "Vadodara, Gujarat, India",
            "linkedin": "https://linkedin.com/in/karinarohra-485282214",
            "availability": "Immediately",
        },
        "summary": (
            "Entry-level digital marketing professional with practical exposure to social media, "
            "SEO, content creation, email marketing, campaign support, keyword research, market "
            "research, competitor analysis, and basic performance reporting."
        ),
        "skill_groups": [
            {
                "category": "SEO",
                "items": ["Keyword Research", "On-Page SEO", "Meta Descriptions", "Title Tags"],
            },
            {
                "category": "Social Media",
                "items": ["Instagram", "LinkedIn", "Content Planning", "Captions"],
            },
        ],
        "experience": [
            {
                "title": "Digital Marketing Intern",
                "organization": "Ofcoursesocial",
                "location": "Vadodara, Gujarat, India",
                "dates": "May 2022 - July 2022",
                "bullets": [
                    "Supported day-to-day digital marketing work across social media, SEO, blogs, landing pages, content planning, and campaign execution.",
                    "Assisted with keyword research and on-page SEO tasks, including meta descriptions, title tags, headings, and content updates.",
                ],
            }
        ],
        "education": [
            {
                "credential": "Master of Business Administration - Digital Marketing",
                "institution": "Dr. D Y Patil Vidyapeeth - Centre for Online Learning",
                "dates": "Jan 2026 - Mar 2028",
                "notes": ["Currently pursuing"],
            }
        ],
        "certifications": ["Digital Marketing Certification - HubSpot Academy"],
        "tailoring": {
            "company": "Self Test",
            "role": "SEO Executive",
        },
    }


def self_test() -> None:
    master_hash = hashlib.sha256(MASTER_RESUME.read_bytes()).hexdigest()
    resume = canonical_test_resume()
    with tempfile.TemporaryDirectory() as directory:
        destination = Path(directory) / "Karina_Rohra_Self_Test_SEO_Executive.pdf"
        build(resume, destination)
        refused = False
        try:
            assert_safe_output(MASTER_RESUME)
        except ResumeBuildError:
            refused = True
        if not refused:
            fail("master-resume overwrite guard did not refuse")
        markdown_refused = False
        try:
            assert_safe_output(Path(directory) / "resume.md")
        except ResumeBuildError:
            markdown_refused = True
        if not markdown_refused:
            fail("non-PDF resume output was accepted")
    if hashlib.sha256(MASTER_RESUME.read_bytes()).hexdigest() != master_hash:
        fail("self-test changed the master resume")


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build and validate a tailored resume PDF.")
    parser.add_argument("--input", type=Path, help="Structured resume JSON. Never attach this file.")
    parser.add_argument("--output", type=Path, help="Destination PDF path outside reference/.")
    parser.add_argument("--validate", type=Path, help="Open an existing PDF and check its text.")
    parser.add_argument(
        "--require-text",
        action="append",
        default=[],
        help="Text that must appear in a PDF checked with --validate. Repeat for each snippet.",
    )
    parser.add_argument(
        "--self-test",
        action="store_true",
        help="Generate a temporary PDF from verified facts and delete it.",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv if argv is not None else sys.argv[1:])
    try:
        if args.self_test:
            self_test()
            print("self-test passed")
        if args.validate:
            validate_pdf(args.validate, required_text=args.require_text)
            print(f"validated PDF: {args.validate}")
        if args.input:
            resume = load_resume(args.input)
            destination = args.output or default_output_path(resume)
            produced = build(resume, destination)
            print(f"wrote validated PDF: {produced}")
        if not args.self_test and not args.validate and not args.input:
            fail("choose --input, --validate, or --self-test")
    except ResumeBuildError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
