#!/usr/bin/env python3
"""Build a truthful tailored resume PDF from structured JSON.

The JSON file is builder input only. Never attach JSON, Markdown, or TXT
as the resume. This script refuses to overwrite the master resume.

Every PDF written by this script must pass two checks before it reaches its
destination path:

* visual: the file is a real PDF that opens, has pages, and every character
  it draws has a glyph in the font that draws it; and
* machine-readable: the text layer that an ATS extracts is clean. Two
  independent extraction passes must return the candidate name, the target
  job title, the core marketing keywords, every employer, education entry and
  tailored sentence, with no replacement characters, control characters,
  mojibake or other encoding anomalies, and every font must carry a Unicode
  mapping.

If the first rendering fails, the PDF is regenerated with an ATS-safe profile
(standard Helvetica, strict ASCII text) and checked again. A PDF that fails is
deleted, never stored.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
import tempfile
import unicodedata
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Callable
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

# ATS keywords that every tailored resume for this candidate must expose in
# its machine-readable text layer. "Digital Marketing" is always required; at
# least one focus keyword must be present in the tailored content.
ATS_CORE_KEYWORD = "Digital Marketing"
ATS_FOCUS_KEYWORDS = ("Social Media", "SEO", "Content Marketing")

SECTION_HEADINGS = {
    "summary": "PROFESSIONAL SUMMARY",
    "skills": "CORE SKILLS",
    "experience": "PROFESSIONAL EXPERIENCE",
    "ai": "AI-ASSISTED DIGITAL MARKETING EXPERIENCE",
    "education": "EDUCATION",
    "certifications": "CERTIFICATIONS & TRAINING",
    "portfolio": "PORTFOLIO",
}
PORTFOLIO_LEAD = "Portfolio and samples available on request, including:"

# Characters a tailored resume may legitimately contain, and which every
# common ATS parser maps unambiguously. Anything outside this set in the
# extracted text is treated as an encoding anomaly.
ATS_ALLOWED_CHARS = frozenset(
    {chr(code) for code in range(0x20, 0x7F)}
    | {chr(code) for code in range(0xC0, 0x100)} - {"\u00d7", "\u00f7"}
    | set("\u00a3\u00a9\u00ae\u00b0\u20ac\u20b9\u2013\u2014\u2018\u2019\u201c\u201d\u2022\u2026")
)
ALLOWED_WHITESPACE = frozenset("\t\n\r\u00a0")

# Reversible-meaning replacements used by the ATS-safe profile so that the
# whole resume is plain ASCII drawn with a standard, non-embedded font.
ASCII_REPLACEMENTS = {
    "\u2018": "'",
    "\u2019": "'",
    "\u201a": "'",
    "\u2032": "'",
    "\u201c": '"',
    "\u201d": '"',
    "\u201e": '"',
    "\u2033": '"',
    "\u2010": "-",
    "\u2011": "-",
    "\u2012": "-",
    "\u2013": "-",
    "\u2014": "-",
    "\u2212": "-",
    "\u2022": "-",
    "\u00b7": "-",
    "\u2026": "...",
    "\u2192": "->",
    "\u00d7": "x",
    "\u00b0": " degrees",
    "\u00a9": "(c)",
    "\u00ae": "(R)",
    "\u2122": "(TM)",
    "\u20b9": "INR ",
    "\u20ac": "EUR ",
    "\u00a3": "GBP ",
    "\u00e6": "ae",
    "\u00c6": "AE",
    "\u0153": "oe",
    "\u0152": "OE",
    "\u00df": "ss",
    "\u00f8": "o",
    "\u00d8": "O",
    "\u0142": "l",
    "\u0141": "L",
    "\u00f0": "d",
    "\u00d0": "D",
    "\u00fe": "th",
    "\u00de": "Th",
}

NON_TEXT_CATEGORIES = frozenset({"Cc", "Cf", "Co", "Cs", "Cn"})

STANDARD_14_FONTS = frozenset(
    {
        "Courier",
        "Courier-Bold",
        "Courier-Oblique",
        "Courier-BoldOblique",
        "Helvetica",
        "Helvetica-Bold",
        "Helvetica-Oblique",
        "Helvetica-BoldOblique",
        "Times-Roman",
        "Times-Bold",
        "Times-Italic",
        "Times-BoldItalic",
        "Symbol",
        "ZapfDingbats",
    }
)
SYMBOLIC_STANDARD_FONTS = frozenset({"Symbol", "ZapfDingbats"})
TEXT_ENCODING_NAMES = frozenset({"/WinAnsiEncoding", "/MacRomanEncoding", "/StandardEncoding"})

MOJIBAKE_PATTERN = re.compile(r"\u00c3[\u0080-\u00bf\u2018-\u201e\u20ac\u2122]|\u00e2\u20ac|\u00c2[\u00a0-\u00bf]")
MALFORMED_WORD_PATTERN = re.compile(r"[A-Za-z]{2,}[\\^~_=<>\[\]{}|*#]+[A-Za-z]{2,}")
REPEATED_SYMBOL_PATTERN = re.compile(r"([^\w\s.\-])\1{2,}")
CID_MARKER_PATTERN = re.compile(r"\(cid:\d+\)")
MIN_LETTER_RATIO = 0.6
MAX_RUN_ON_WORD = 60


class ResumeBuildError(Exception):
    """A truthful-resume check failed."""


def fail(message: str) -> None:
    raise ResumeBuildError(message)


def normalize_space(value: str) -> str:
    return re.sub(r"\s+", " ", value).strip()


def squash(value: str) -> str:
    """Whitespace-insensitive, case-insensitive form used to compare extractors."""
    return re.sub(r"\s+", "", value).casefold()


def sanitize_text(value: str) -> str:
    """Normalise builder text without changing its meaning.

    Composes characters (NFC), turns non-breaking spaces into spaces and drops
    invisible control/format characters such as zero-width spaces or soft
    hyphens that are common in text copied from web pages.
    """
    text = unicodedata.normalize("NFC", value).replace("\u00a0", " ")
    text = "".join(
        ch for ch in text if ch in "\t\n" or unicodedata.category(ch) not in NON_TEXT_CATEGORIES
    )
    return normalize_space(text)


def transliterate_ascii(value: str) -> str:
    """Return a strict-ASCII rendering of the text for the ATS-safe profile.

    Typographic punctuation becomes its ASCII equivalent and accented Latin
    letters lose their diacritics. Any character that cannot be represented
    stops the build rather than being guessed.
    """
    text = sanitize_text(value)
    text = "".join(ASCII_REPLACEMENTS.get(ch, ch) for ch in text)
    text = unicodedata.normalize("NFKD", text)
    text = "".join(ch for ch in text if not unicodedata.combining(ch))
    unmappable = sorted({ch for ch in text if ord(ch) > 0x7E or (ord(ch) < 0x20 and ch not in "\t\n")})
    if unmappable:
        rendered = ", ".join(f"U+{ord(ch):04X} {ch!r}" for ch in unmappable)
        fail(f"text cannot be represented in ATS-safe ASCII: {rendered}")
    return normalize_space(text)


@dataclass(frozen=True)
class FontProfile:
    """How text is drawn into the PDF and which text layer that produces."""

    name: str
    description: str
    regular: str
    bold: str
    italic: str
    bullet: str
    embedded: bool
    text: Callable[[str], str]


def register_embedded_fonts() -> None:
    """Register the Bitstream Vera TrueType family shipped with reportlab.

    Embedded TrueType subsets carry a /ToUnicode CMap, so every glyph maps
    back to the exact Unicode character that was drawn.
    """
    try:
        import reportlab
        from reportlab.pdfbase import pdfmetrics
        from reportlab.pdfbase.ttfonts import TTFont
    except ImportError as exc:
        fail(f"reportlab is not installed ({exc}). Install requirements.txt.")
    if "ResumeSans" in pdfmetrics.getRegisteredFontNames():
        return
    font_dir = Path(reportlab.__file__).resolve().parent / "fonts"
    files = {
        "ResumeSans": "Vera.ttf",
        "ResumeSans-Bold": "VeraBd.ttf",
        "ResumeSans-Italic": "VeraIt.ttf",
        "ResumeSans-BoldItalic": "VeraBI.ttf",
    }
    for font_name, file_name in files.items():
        path = font_dir / file_name
        if not path.is_file():
            fail(f"embedded font file is missing: {path}")
        pdfmetrics.registerFont(TTFont(font_name, str(path)))
    pdfmetrics.registerFontFamily(
        "ResumeSans",
        normal="ResumeSans",
        bold="ResumeSans-Bold",
        italic="ResumeSans-Italic",
        boldItalic="ResumeSans-BoldItalic",
    )


EMBEDDED_UNICODE_PROFILE = FontProfile(
    name="embedded-unicode",
    description="embedded TrueType (Bitstream Vera) with a /ToUnicode map; text normalised, meaning unchanged",
    regular="ResumeSans",
    bold="ResumeSans-Bold",
    italic="ResumeSans-Italic",
    bullet="\u2022",
    embedded=True,
    text=sanitize_text,
)

ATS_SAFE_ASCII_PROFILE = FontProfile(
    name="ats-safe-ascii",
    description="standard Helvetica (WinAnsi, not embedded) with strict ASCII text",
    regular="Helvetica",
    bold="Helvetica-Bold",
    italic="Helvetica-Oblique",
    bullet="-",
    embedded=False,
    text=transliterate_ascii,
)

FONT_PROFILES = {
    EMBEDDED_UNICODE_PROFILE.name: EMBEDDED_UNICODE_PROFILE,
    ATS_SAFE_ASCII_PROFILE.name: ATS_SAFE_ASCII_PROFILE,
}
# Order in which build() tries profiles: the first that passes wins.
PROFILE_SEQUENCE = (EMBEDDED_UNICODE_PROFILE, ATS_SAFE_ASCII_PROFILE)


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


@dataclass(frozen=True)
class Block:
    """One paragraph of the resume.

    ``text`` is the content an ATS must be able to extract, ``drawn`` is the
    exact string painted into the PDF (including any bullet marker) and
    ``markup`` is the reportlab paragraph markup used to paint it.
    """

    style: str
    text: str
    drawn: str
    markup: str
    label: str


def _block(style: str, text: str, label: str, prefix: str = "", markup: str | None = None) -> Block:
    drawn = f"{prefix}{text}" if prefix else text
    return Block(style, text, drawn, markup if markup is not None else escape(drawn), label)


def compose(resume: dict, profile: FontProfile) -> list[Block]:
    """Turn the structured resume into the ordered paragraphs that get drawn."""
    text = profile.text
    bullet_prefix = f"{profile.bullet} "
    contact = resume["contact"]
    contact_bits = [contact["email"], contact["phone"], contact["location"], contact["linkedin"]]
    if contact.get("availability"):
        contact_bits.append(f"Available: {contact['availability']}")

    blocks = [
        _block("name", text(resume["candidate_name"]), "candidate name"),
        _block("headline", text(resume["headline"]), "headline"),
    ]
    blocks.extend(_block("contact", text(bit), "contact detail") for bit in contact_bits)
    blocks.append(_block("rule", "", "divider"))
    blocks.append(_block("section", SECTION_HEADINGS["summary"], "section heading"))
    blocks.append(_block("body", text(resume["summary"]), "summary"))
    blocks.append(_block("section", SECTION_HEADINGS["skills"], "section heading"))
    for group in resume["skill_groups"]:
        category = text(group["category"])
        items = text(", ".join(group["items"]))
        blocks.append(
            _block(
                "body",
                f"{category}: {items}",
                "skill group",
                markup=f"<b>{escape(category)}:</b> {escape(items)}",
            )
        )

    blocks.append(_block("section", SECTION_HEADINGS["experience"], "section heading"))
    for item in resume["experience"]:
        blocks.append(_block("role", text(item["title"]), "experience title"))
        blocks.append(
            _block(
                "meta",
                text(f"{item['organization']} | {item['location']} | {item['dates']}"),
                "experience employer",
            )
        )
        blocks.extend(
            _block("bullet", text(bullet), "experience bullet", prefix=bullet_prefix)
            for bullet in item["bullets"]
        )

    if resume.get("ai_assisted_bullets"):
        blocks.append(_block("section", SECTION_HEADINGS["ai"], "section heading"))
        blocks.extend(
            _block("bullet", text(bullet), "AI-assisted bullet", prefix=bullet_prefix)
            for bullet in resume["ai_assisted_bullets"]
        )

    blocks.append(_block("section", SECTION_HEADINGS["education"], "section heading"))
    for item in resume["education"]:
        blocks.append(_block("role", text(item["credential"]), "education credential"))
        blocks.append(
            _block("meta", text(f"{item['institution']} | {item['dates']}"), "education institution")
        )
        blocks.extend(_block("body", text(note), "education note") for note in item.get("notes", []))

    blocks.append(_block("section", SECTION_HEADINGS["certifications"], "section heading"))
    blocks.extend(
        _block("bullet", text(item), "certification", prefix=bullet_prefix)
        for item in resume["certifications"]
    )

    if resume.get("portfolio_items"):
        blocks.append(_block("section", SECTION_HEADINGS["portfolio"], "section heading"))
        blocks.append(_block("body", PORTFOLIO_LEAD, "portfolio lead"))
        blocks.extend(
            _block("bullet", text(item), "portfolio item", prefix=bullet_prefix)
            for item in resume["portfolio_items"]
        )
    return blocks


def assert_glyph_coverage(blocks: list[Block], profile: FontProfile) -> None:
    """Visual check before drawing: every character must exist in the font.

    Embedded TrueType fonts paint a .notdef box for a missing glyph while the
    text layer still looks right, so this is checked up front. Standard fonts
    only receive ASCII in the ATS-safe profile, which they always cover.
    """
    if not profile.embedded:
        return
    from reportlab.pdfbase import pdfmetrics

    drawn = "".join(block.drawn for block in blocks)
    missing: set[str] = set()
    for font_name in (profile.regular, profile.bold, profile.italic):
        char_map = pdfmetrics.getFont(font_name).face.charToGlyph
        missing.update(ch for ch in drawn if not ch.isspace() and ord(ch) not in char_map)
    if missing:
        rendered = ", ".join(f"U+{ord(ch):04X} {ch!r}" for ch in sorted(missing))
        fail(f"font profile {profile.name} has no glyph for: {rendered}")


def render_pdf(resume: dict, destination: Path, profile: FontProfile = EMBEDDED_UNICODE_PROFILE) -> list[Block]:
    try:
        from reportlab.lib.colors import HexColor
        from reportlab.lib.enums import TA_LEFT
        from reportlab.lib.pagesizes import A4
        from reportlab.lib.styles import ParagraphStyle
        from reportlab.lib.units import inch
        from reportlab.platypus import HRFlowable, Paragraph, SimpleDocTemplate
    except ImportError as exc:
        fail(f"reportlab is not installed ({exc}). Install requirements.txt.")

    if profile.embedded:
        register_embedded_fonts()
    blocks = compose(resume, profile)
    assert_glyph_coverage(blocks, profile)

    styles = {
        "name": ParagraphStyle(
            "Name",
            fontName=profile.bold,
            fontSize=16,
            leading=19,
            alignment=TA_LEFT,
            textColor=HexColor("#1F2933"),
            spaceAfter=2,
        ),
        "headline": ParagraphStyle(
            "Headline",
            fontName=profile.italic,
            fontSize=10,
            leading=13,
            textColor=HexColor("#334E68"),
            spaceAfter=4,
        ),
        "contact": ParagraphStyle(
            "Contact",
            fontName=profile.regular,
            fontSize=9,
            leading=12,
            spaceAfter=8,
        ),
        "section": ParagraphStyle(
            "Section",
            fontName=profile.bold,
            fontSize=11,
            leading=14,
            textColor=HexColor("#1F2933"),
            spaceBefore=8,
            spaceAfter=3,
        ),
        "body": ParagraphStyle(
            "Body",
            fontName=profile.regular,
            fontSize=10,
            leading=13,
            spaceAfter=4,
        ),
        "role": ParagraphStyle(
            "Role",
            fontName=profile.bold,
            fontSize=10.5,
            leading=13,
            spaceBefore=4,
            spaceAfter=0,
        ),
        "meta": ParagraphStyle(
            "Meta",
            fontName=profile.italic,
            fontSize=9.5,
            leading=12,
            spaceAfter=2,
        ),
        "bullet": ParagraphStyle(
            "Bullet",
            fontName=profile.regular,
            fontSize=10,
            leading=13,
            leftIndent=12,
            bulletIndent=0,
            spaceAfter=1,
        ),
    }

    story = []
    contact_markup: list[str] = []
    for block in blocks:
        if block.style == "contact":
            contact_markup.append(block.markup)
            continue
        if contact_markup:
            story.append(Paragraph(" | ".join(contact_markup), styles["contact"]))
            contact_markup = []
        if block.style == "rule":
            story.append(HRFlowable(width="100%", thickness=0.6, color=HexColor("#9FB3C8"), spaceAfter=4))
        else:
            story.append(Paragraph(block.markup, styles[block.style]))

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
    return blocks


def open_pdf(path: Path):
    """Confirm the file is a real, readable PDF and return the reader."""
    if not path.is_file():
        fail(f"PDF does not exist: {path}")
    header = path.read_bytes()[:5]
    if header != b"%PDF-":
        fail(f"file is not a PDF: {path}")
    try:
        from pypdf import PdfReader
    except ImportError as exc:
        fail(f"pypdf is not installed ({exc}). Install requirements.txt.")
    try:
        reader = PdfReader(str(path))
        if reader.is_encrypted:
            fail(f"PDF is encrypted and cannot be read by an ATS: {path}")
        page_count = len(reader.pages)
        if page_count < 1:
            fail(f"PDF has no pages: {path}")
        for index, page in enumerate(reader.pages, start=1):
            box = page.mediabox
            if float(box.width) <= 0 or float(box.height) <= 0:
                fail(f"PDF page {index} has an empty page size")
    except ResumeBuildError:
        raise
    except Exception as exc:
        fail(f"PDF could not be opened: {exc}")
    return reader


def extract_pdf_text(path: Path) -> str:
    """Primary text extraction: the parser the pipeline already relies on."""
    reader = open_pdf(path)
    try:
        return "\n".join((page.extract_text() or "") for page in reader.pages)
    except Exception as exc:
        fail(f"PDF text could not be extracted: {exc}")


def extract_pdf_text_independent(path: Path) -> str:
    """Second extraction pass using pypdf's layout engine.

    The layout engine resolves fonts, encodings and glyph positions through
    its own code path, so agreement between both passes is evidence that the
    text layer is not an artefact of one algorithm.
    """
    reader = open_pdf(path)
    try:
        return "\n".join(
            (page.extract_text(extraction_mode="layout") or "") for page in reader.pages
        )
    except Exception as exc:
        fail(f"independent PDF text extraction failed: {exc}")


def _font_base_name(font: dict) -> str:
    base = str(font.get("/BaseFont", "")).lstrip("/")
    if len(base) > 7 and base[6] == "+" and base[:6].isalpha() and base[:6].isupper():
        base = base[7:]
    return base


def _encoding_is_textual(encoding) -> bool:
    if encoding is None:
        return False
    if hasattr(encoding, "get_object"):
        encoding = encoding.get_object()
    if isinstance(encoding, str):
        return encoding in TEXT_ENCODING_NAMES
    try:
        base = encoding.get("/BaseEncoding")
    except AttributeError:
        return False
    return base is None or str(base) in TEXT_ENCODING_NAMES


def _iter_fonts(resources, seen: set, depth: int = 0):
    if resources is None or depth > 8:
        return
    if hasattr(resources, "get_object"):
        resources = resources.get_object()
    fonts = resources.get("/Font")
    if fonts is not None:
        if hasattr(fonts, "get_object"):
            fonts = fonts.get_object()
        for key, ref in fonts.items():
            ident = getattr(ref, "idnum", None) or (depth, str(key))
            if ident in seen:
                continue
            seen.add(ident)
            yield str(key), ref.get_object() if hasattr(ref, "get_object") else ref
    xobjects = resources.get("/XObject")
    if xobjects is not None:
        if hasattr(xobjects, "get_object"):
            xobjects = xobjects.get_object()
        for ref in xobjects.values():
            xobject = ref.get_object() if hasattr(ref, "get_object") else ref
            if str(xobject.get("/Subtype")) == "/Form":
                yield from _iter_fonts(xobject.get("/Resources"), seen, depth + 1)


def audit_pdf_fonts(path: Path) -> tuple[list[str], list[str]]:
    """Structural check that every font maps its glyphs back to Unicode.

    Returns (font descriptions, problems). A font is acceptable when it has a
    /ToUnicode CMap, or when it is one of the standard 14 text fonts drawn with
    a standard textual encoding. Type3 fonts, symbolic fonts and fonts without
    any Unicode mapping are what produce garbage in an ATS.
    """
    reader = open_pdf(path)
    descriptions: list[str] = []
    problems: list[str] = []
    seen: set = set()
    for page_number, page in enumerate(reader.pages, start=1):
        try:
            resources = page.get("/Resources")
        except Exception as exc:
            problems.append(f"page {page_number}: resources could not be read ({exc})")
            continue
        for key, font in _iter_fonts(resources, seen):
            subtype = str(font.get("/Subtype", ""))
            base = _font_base_name(font) or "(unnamed)"
            has_to_unicode = "/ToUnicode" in font
            encoding = font.get("/Encoding")
            encoding_text = str(encoding) if isinstance(encoding, str) else ("dict" if encoding is not None else "none")
            descriptions.append(
                f"{base} ({subtype.lstrip('/')}, encoding={encoding_text.lstrip('/')}, ToUnicode={'yes' if has_to_unicode else 'no'})"
            )
            if subtype == "/Type3":
                problems.append(f"font {key} {base} is a Type3 font, which ATS parsers cannot map to text")
                continue
            if base in SYMBOLIC_STANDARD_FONTS:
                problems.append(f"font {key} {base} is a symbolic font; its glyphs do not map to real text")
                continue
            if has_to_unicode:
                continue
            if subtype == "/Type0":
                problems.append(f"font {key} {base} is a composite font without a /ToUnicode map")
                continue
            if base in STANDARD_14_FONTS and _encoding_is_textual(encoding):
                continue
            if subtype in {"/Type1", "/TrueType", "/MMType1"} and isinstance(encoding, str) and encoding in TEXT_ENCODING_NAMES:
                continue
            problems.append(f"font {key} {base} has no Unicode mapping (no /ToUnicode and no standard text encoding)")
    if not descriptions:
        problems.append("PDF declares no fonts; its text is not selectable")
    return descriptions, problems


def find_text_anomalies(text: str) -> list[str]:
    """Detect encoding corruption in extracted text."""
    issues: list[str] = []
    if not text.strip():
        return ["no text could be extracted"]

    replacement_count = text.count("\ufffd")
    if replacement_count:
        issues.append(f"replacement character U+FFFD appears {replacement_count} time(s)")

    controls = sorted({ch for ch in text if unicodedata.category(ch) == "Cc" and ch not in ALLOWED_WHITESPACE})
    if controls:
        issues.append("control characters in text layer: " + ", ".join(f"U+{ord(ch):04X}" for ch in controls))

    non_text = sorted(
        {
            ch
            for ch in text
            if ch not in ALLOWED_WHITESPACE
            and ch not in controls
            and unicodedata.category(ch) in NON_TEXT_CATEGORIES
        }
    )
    if non_text:
        issues.append(
            "private-use, format or unassigned characters: " + ", ".join(f"U+{ord(ch):04X}" for ch in non_text)
        )

    if CID_MARKER_PATTERN.search(text):
        issues.append("unmapped glyph markers such as (cid:NN) are present")
    if MOJIBAKE_PATTERN.search(text):
        issues.append("mojibake sequences (mis-decoded UTF-8 such as 'Ã©' or 'â€™') are present")

    unexpected = sorted(
        {
            ch
            for ch in text
            if ch not in ATS_ALLOWED_CHARS
            and ch not in ALLOWED_WHITESPACE
            and ch not in controls
            and ch not in non_text
            and ch != "\ufffd"
        }
    )
    if unexpected:
        rendered = ", ".join(f"U+{ord(ch):04X} {ch!r}" for ch in unexpected[:12])
        issues.append(f"characters outside the ATS-safe set: {rendered}")

    visible = [ch for ch in text if not ch.isspace()]
    if visible:
        letters = sum(1 for ch in visible if ch.isalpha())
        ratio = letters / len(visible)
        if ratio < MIN_LETTER_RATIO:
            issues.append(f"text is only {ratio:.0%} letters; expected readable prose")

    malformed = sorted({match.group(0) for match in MALFORMED_WORD_PATTERN.finditer(text)})
    if malformed:
        issues.append("malformed words: " + ", ".join(malformed[:8]))
    repeated = sorted({match.group(0) for match in REPEATED_SYMBOL_PATTERN.finditer(text)})
    if repeated:
        issues.append("repeated symbol runs: " + ", ".join(repeated[:8]))
    run_on = [
        token
        for token in re.findall(r"\S+", text)
        if len(token) > MAX_RUN_ON_WORD and not any(mark in token for mark in ("/", "@", "."))
    ]
    if run_on:
        issues.append("run-on words with no spaces: " + ", ".join(token[:40] + "..." for token in run_on[:3]))
    return issues


def expected_snippets(resume: dict, profile: FontProfile) -> list[tuple[str, str]]:
    """Every string an ATS must find in the text layer, labelled."""
    snippets: list[tuple[str, str]] = [
        ("candidate name", CANDIDATE_NAME),
        ("target job title", profile.text(resume["tailoring"]["role"])),
        ("core keyword", ATS_CORE_KEYWORD),
    ]
    content = squash(json.dumps(resume, ensure_ascii=False))
    focus_present = [keyword for keyword in ATS_FOCUS_KEYWORDS if squash(keyword) in content]
    snippets.extend(("focus keyword", keyword) for keyword in focus_present)
    for block in compose(resume, profile):
        if block.text:
            snippets.append((block.label, block.text))
    return snippets


def assert_ats_content(resume: dict) -> None:
    """Pre-render checks on the tailored content itself."""
    role = squash(resume["tailoring"]["role"])
    if role not in squash(resume["headline"]) and role not in squash(resume["summary"]):
        fail(
            "the headline or summary must name the target job title "
            f"'{resume['tailoring']['role']}' so an ATS can match it"
        )
    content = squash(json.dumps(resume, ensure_ascii=False))
    if squash(ATS_CORE_KEYWORD) not in content:
        fail(f"tailored resume never mentions '{ATS_CORE_KEYWORD}'")
    if not any(squash(keyword) in content for keyword in ATS_FOCUS_KEYWORDS):
        fail("tailored resume mentions none of " + ", ".join(ATS_FOCUS_KEYWORDS))


@dataclass
class AtsCheckReport:
    """Outcome of the visual and machine-readable validation of one PDF."""

    pdf: str
    font_profile: str | None
    pages: int = 0
    fonts: list[str] = field(default_factory=list)
    primary_characters: int = 0
    independent_characters: int = 0
    snippets_checked: int = 0
    problems: list[str] = field(default_factory=list)
    regenerated_after: list[str] = field(default_factory=list)

    @property
    def passed(self) -> bool:
        return not self.problems

    def to_dict(self) -> dict:
        data = asdict(self)
        data["passed"] = self.passed
        return data

    def summary(self) -> str:
        status = "PASS" if self.passed else "FAIL"
        lines = [
            f"ATS check {status}: {self.pdf}",
            f"  font profile: {self.font_profile or 'unknown'}",
            f"  pages: {self.pages}; fonts: {'; '.join(self.fonts) or 'none'}",
            f"  text layer: {self.primary_characters} characters (primary), "
            f"{self.independent_characters} characters (independent)",
            f"  expected snippets verified: {self.snippets_checked}",
        ]
        lines.extend(f"  regenerated after: {attempt}" for attempt in self.regenerated_after)
        lines.extend(f"  problem: {problem}" for problem in self.problems)
        return "\n".join(lines)


def ats_check_pdf(
    path: Path,
    resume: dict | None = None,
    required_text: list[str] | None = None,
    profile: FontProfile | None = None,
) -> AtsCheckReport:
    """Run the full visual and machine-readable validation without raising."""
    report = AtsCheckReport(pdf=str(path), font_profile=profile.name if profile else None)
    try:
        reader = open_pdf(path)
        report.pages = len(reader.pages)
        report.fonts, font_problems = audit_pdf_fonts(path)
        report.problems.extend(font_problems)
        primary = extract_pdf_text(path)
        independent = extract_pdf_text_independent(path)
    except ResumeBuildError as exc:
        report.problems.append(str(exc))
        return report

    report.primary_characters = len(primary)
    report.independent_characters = len(independent)

    for page_number, page in enumerate(reader.pages, start=1):
        page_text = page.extract_text() or ""
        if not any(ch.isalnum() for ch in page_text):
            report.problems.append(f"page {page_number} has no extractable text")

    report.problems.extend(f"primary extraction: {issue}" for issue in find_text_anomalies(primary))
    independent_issues = [
        issue for issue in find_text_anomalies(independent) if not issue.startswith("run-on words")
    ]
    report.problems.extend(f"independent extraction: {issue}" for issue in independent_issues)

    snippets: list[tuple[str, str]] = []
    if resume is not None:
        snippets.extend(expected_snippets(resume, profile or EMBEDDED_UNICODE_PROFILE))
    else:
        snippets.append(("candidate name", CANDIDATE_NAME))
        snippets.append(("core keyword", ATS_CORE_KEYWORD))
    snippets.extend(("required text", item) for item in (required_text or []))

    folded_primary = normalize_space(primary).casefold()
    squashed_primary = squash(primary)
    squashed_independent = squash(independent)
    for label, snippet in snippets:
        wanted = normalize_space(snippet)
        if not wanted:
            continue
        if wanted.casefold() not in folded_primary:
            if squash(wanted) in squashed_primary:
                report.problems.append(f"{label} is extracted with broken word spacing: {wanted[:80]}")
            else:
                report.problems.append(f"{label} is missing or corrupted in the text layer: {wanted[:80]}")
        if squash(wanted) not in squashed_independent:
            report.problems.append(f"{label} is missing from the independent extraction: {wanted[:80]}")
    report.snippets_checked = len(snippets)

    if resume is None and not any(squash(keyword) in squashed_primary for keyword in ATS_FOCUS_KEYWORDS):
        report.problems.append("none of the focus keywords " + ", ".join(ATS_FOCUS_KEYWORDS) + " is extractable")
    return report


def validate_pdf(
    path: Path,
    resume: dict | None = None,
    required_text: list[str] | None = None,
    profile: FontProfile | None = None,
) -> str:
    """Raise unless the PDF passes the visual and machine-readable checks."""
    report = ats_check_pdf(path, resume=resume, required_text=required_text, profile=profile)
    if not report.passed:
        fail("PDF failed the machine-readable check: " + " | ".join(report.problems))
    return extract_pdf_text(path)


def default_output_path(resume: dict) -> Path:
    company = re.sub(r"[^A-Za-z0-9]+", "_", resume["tailoring"]["company"]).strip("_")
    role = re.sub(r"[^A-Za-z0-9]+", "_", resume["tailoring"]["role"]).strip("_")
    company = (company or "Company")[:40]
    role = (role or "Role")[:40]
    return REPO_ROOT / "output" / "resumes" / f"Karina_Rohra_{company}_{role}.pdf"


def build_with_report(
    resume: dict,
    destination: Path,
    profiles: tuple[FontProfile, ...] = PROFILE_SEQUENCE,
) -> tuple[Path, AtsCheckReport]:
    """Render, validate and only then move the PDF to its destination.

    Profiles are tried in order. Each attempt is rendered to a hidden
    temporary file beside the destination, checked visually and for
    machine-readability, and either moved into place or deleted. The
    destination therefore only ever holds a PDF that passed both checks.
    """
    assert_truthful(resume)
    assert_ats_content(resume)
    output = assert_safe_output(destination)
    master_hash = hashlib.sha256(MASTER_RESUME.read_bytes()).hexdigest()
    if output.exists():
        output.unlink()

    attempts: list[str] = []
    for profile in profiles:
        handle, temp_name = tempfile.mkstemp(dir=output.parent, prefix=".pending-", suffix=".pdf")
        os.close(handle)
        pending = Path(temp_name)
        try:
            render_pdf(resume, pending, profile)
            report = ats_check_pdf(pending, resume=resume, profile=profile)
        except ResumeBuildError as exc:
            pending.unlink(missing_ok=True)
            attempts.append(f"{profile.name}: {exc}")
            continue
        if report.passed:
            os.chmod(pending, 0o644)
            os.replace(pending, output)
            report.pdf = str(output)
            if hashlib.sha256(MASTER_RESUME.read_bytes()).hexdigest() != master_hash:
                output.unlink(missing_ok=True)
                fail("master resume changed during PDF generation")
            report.regenerated_after = attempts
            return output, report
        pending.unlink(missing_ok=True)
        attempts.append(f"{profile.name}: " + "; ".join(report.problems))

    fail("no PDF passed the visual and machine-readable checks; nothing was stored. " + " || ".join(attempts))


def build(resume: dict, destination: Path, profiles: tuple[FontProfile, ...] = PROFILE_SEQUENCE) -> Path:
    return build_with_report(resume, destination, profiles)[0]


def canonical_test_resume() -> dict:
    return {
        "candidate_name": CANDIDATE_NAME,
        "headline": "SEO Executive | Digital Marketing | Social Media | Content Marketing",
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


def expect_refusal(action: Callable[[], object], message: str, fragment: str | None = None) -> None:
    try:
        action()
    except ResumeBuildError as exc:
        if fragment and fragment not in str(exc):
            fail(f"{message}: refused for an unexpected reason: {exc}")
        return
    fail(message)


def _strip_to_unicode(source: Path, destination: Path) -> None:
    """Write a copy of a PDF whose embedded fonts lose their /ToUnicode maps.

    The pages look identical, but the glyph codes no longer map to Unicode,
    which is the classic 'looks fine, parses as garbage' ATS failure.
    """
    from pypdf import PdfReader, PdfWriter
    from pypdf.generic import NameObject

    reader = PdfReader(str(source))
    writer = PdfWriter()
    writer.append(reader)
    for page in writer.pages:
        fonts = page["/Resources"]["/Font"]
        for ref in fonts.values():
            font = ref.get_object()
            if NameObject("/ToUnicode") in font:
                del font[NameObject("/ToUnicode")]
    with destination.open("wb") as handle:
        writer.write(handle)


def _draw_symbolic_pdf(destination: Path) -> None:
    """Draw the resume header with the symbolic Symbol font.

    The glyph codes are letters, but the font maps them to Greek characters,
    so the text layer does not contain the candidate name.
    """
    from reportlab.lib.pagesizes import A4
    from reportlab.pdfgen import canvas

    page = canvas.Canvas(str(destination), pagesize=A4)
    page.setFont("Symbol", 11)
    page.drawString(72, 760, f"{CANDIDATE_NAME} Digital Marketing SEO")
    page.save()


def _draw_legacy_bullet_pdf(destination: Path) -> None:
    """Reproduce the old Times-Roman rendering whose bullets extract as DEL."""
    from reportlab.lib.pagesizes import A4
    from reportlab.pdfgen import canvas

    page = canvas.Canvas(str(destination), pagesize=A4)
    page.setFont("Times-Roman", 11)
    page.drawString(72, 760, f"{CANDIDATE_NAME} - Digital Marketing")
    page.drawString(72, 740, "\u2022 Supported SEO and social media content planning.")
    page.save()


def self_test() -> None:
    master_hash = hashlib.sha256(MASTER_RESUME.read_bytes()).hexdigest()
    resume = canonical_test_resume()
    with tempfile.TemporaryDirectory() as directory:
        workdir = Path(directory)

        # 1. A truthful resume renders with the primary profile and its text
        #    layer is exact: bullets are U+2022, no control characters.
        destination = workdir / "Karina_Rohra_Self_Test_SEO_Executive.pdf"
        produced, report = build_with_report(resume, destination)
        if produced != destination or not report.passed:
            fail("self-test build did not produce a validated PDF")
        if report.font_profile != EMBEDDED_UNICODE_PROFILE.name:
            fail("self-test build did not use the primary embedded-unicode profile")
        text = extract_pdf_text(destination)
        if "\u2022" not in text or "\x7f" in text:
            fail("bullets did not round-trip as U+2022 in the text layer")
        if find_text_anomalies(text):
            fail("primary profile text layer reported anomalies: " + "; ".join(find_text_anomalies(text)))
        if list(workdir.glob(".pending-*")):
            fail("temporary pending PDF was left behind")

        # 2. The anomaly detector catches the corruption classes we reject.
        clean = "Karina Rohra \u2022 Digital Marketing \u2013 SEO, Social Media & Content Marketing (2022)."
        if find_text_anomalies(clean):
            fail("anomaly detector flagged clean text: " + "; ".join(find_text_anomalies(clean)))
        corrupt_samples = {
            "replacement": clean + " Marke\ufffding",
            "control": clean + " \x7f Supported",
            "private use": clean + " \ue000 SEO",
            "mojibake": clean + " Ã© â€™",
            "cid": clean + " (cid:12)(cid:40)",
            "malformed": clean + " Mark|eting",
            "garbage": "@@@ ### 123 456 !!! $$$ %%% 789 ^^^",
            "empty": "   ",
        }
        for label, sample in corrupt_samples.items():
            if not find_text_anomalies(sample):
                fail(f"anomaly detector missed {label} corruption")

        # 3. A PDF that looks right but has no Unicode mapping is rejected and
        #    reported by both the font audit and the extraction comparison.
        stripped = workdir / "stripped.pdf"
        _strip_to_unicode(destination, stripped)
        stripped_report = ats_check_pdf(stripped, resume=resume, profile=EMBEDDED_UNICODE_PROFILE)
        if stripped_report.passed:
            fail("PDF without /ToUnicode maps passed the machine-readable check")
        if not any("no Unicode mapping" in problem for problem in stripped_report.problems):
            fail("font audit did not flag the missing /ToUnicode map")
        expect_refusal(
            lambda: validate_pdf(stripped, required_text=[CANDIDATE_NAME]),
            "validate_pdf accepted a PDF with a corrupted text layer",
            "machine-readable",
        )

        # 3b. Text drawn with a symbolic font extracts as different characters
        #     than the ones a reader sees; the name check must notice.
        symbolic = workdir / "symbolic.pdf"
        _draw_symbolic_pdf(symbolic)
        symbolic_report = ats_check_pdf(symbolic, required_text=[CANDIDATE_NAME])
        if symbolic_report.passed:
            fail("PDF drawn with a symbolic font passed the machine-readable check")
        if not any("candidate name is missing or corrupted" in problem for problem in symbolic_report.problems):
            fail("extraction check did not notice the corrupted candidate name")

        # 4. The legacy Times-Roman bullet, which extracted as U+007F, is caught.
        legacy = workdir / "legacy.pdf"
        _draw_legacy_bullet_pdf(legacy)
        legacy_text = extract_pdf_text(legacy)
        if "\x7f" not in legacy_text:
            fail("legacy rendering no longer reproduces the DEL bullet; update the self-test")
        if not any("control characters" in issue for issue in find_text_anomalies(legacy_text)):
            fail("anomaly detector missed the legacy DEL bullet")
        if ats_check_pdf(legacy, required_text=[CANDIDATE_NAME]).passed:
            fail("legacy rendering with a corrupt bullet passed the check")

        # 5. Content the embedded font cannot draw triggers regeneration with
        #    the ATS-safe ASCII profile instead of a corrupt or missing glyph.
        fallback = canonical_test_resume()
        fallback["experience"][0]["bullets"].append(
            "Supported SEO content updates \u2192 landing pages with \u201cclear\u201d copy."
        )
        fallback_destination = workdir / "Karina_Rohra_Fallback_SEO_Executive.pdf"
        _, fallback_report = build_with_report(fallback, fallback_destination)
        if fallback_report.font_profile != ATS_SAFE_ASCII_PROFILE.name:
            fail("unsupported glyph did not trigger the ATS-safe profile")
        if not any("U+2192" in attempt for attempt in fallback_report.regenerated_after):
            fail("fallback report does not record why the first profile was rejected")
        fallback_text = extract_pdf_text(fallback_destination)
        if "->" not in fallback_text or "\u2192" in fallback_text or '"clear"' not in fallback_text:
            fail("ATS-safe profile did not transliterate to ASCII")
        if any(ord(ch) > 0x7E for ch in fallback_text):
            fail("ATS-safe profile produced non-ASCII text")
        fallback_fonts, fallback_font_problems = audit_pdf_fonts(fallback_destination)
        if fallback_font_problems or not any(font.startswith("Helvetica") for font in fallback_fonts):
            fail("ATS-safe profile did not use standard Helvetica fonts")

        # 6. When every profile fails, nothing is stored.
        hopeless = canonical_test_resume()
        hopeless["experience"][0]["bullets"].append("Supported SEO content \u65e5\u672c\u8a9e for a regional campaign.")
        hopeless_destination = workdir / "Karina_Rohra_Hopeless_SEO_Executive.pdf"
        expect_refusal(
            lambda: build(hopeless, hopeless_destination),
            "unrepresentable text was accepted",
            "nothing was stored",
        )
        if hopeless_destination.exists() or list(workdir.glob(".pending-*")):
            fail("a failed PDF was left on disk")

        # 7. A resume that never names the target job title is refused.
        untargeted = canonical_test_resume()
        untargeted["tailoring"]["role"] = "Social Media Coordinator"
        expect_refusal(
            lambda: build(untargeted, workdir / "Karina_Rohra_Untargeted.pdf"),
            "resume without the target job title was accepted",
            "target job title",
        )

        # 8. Existing output guards.
        expect_refusal(lambda: assert_safe_output(MASTER_RESUME), "master-resume overwrite guard did not refuse")
        expect_refusal(lambda: assert_safe_output(workdir / "resume.md"), "non-PDF resume output was accepted")
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
        help="Generate temporary PDFs from verified facts, exercise the ATS checks, and delete them.",
    )
    parser.add_argument(
        "--font-profile",
        choices=sorted(FONT_PROFILES),
        help=(
            "Force one font profile instead of trying embedded-unicode first and "
            "falling back to ats-safe-ascii."
        ),
    )
    parser.add_argument(
        "--report",
        type=Path,
        help="Write the ATS check report as JSON to this path (never attach it as the resume).",
    )
    return parser.parse_args(argv)


def write_report(report: AtsCheckReport, path: Path | None) -> None:
    if path is None:
        return
    if path.suffix.lower() == ".pdf":
        fail("the report path must not look like a resume PDF")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(report.to_dict(), indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv if argv is not None else sys.argv[1:])
    try:
        if args.self_test:
            self_test()
            print("self-test passed")
        if args.validate:
            report = ats_check_pdf(args.validate, required_text=args.require_text)
            print(report.summary())
            write_report(report, args.report)
            if not report.passed:
                fail(f"PDF failed validation: {args.validate}")
            print(f"validated PDF: {args.validate}")
        if args.input:
            resume = load_resume(args.input)
            destination = args.output or default_output_path(resume)
            profiles = (FONT_PROFILES[args.font_profile],) if args.font_profile else PROFILE_SEQUENCE
            produced, report = build_with_report(resume, destination, profiles)
            print(report.summary())
            write_report(report, args.report)
            print(f"wrote validated PDF: {produced}")
        if not args.self_test and not args.validate and not args.input:
            fail("choose --input, --validate, or --self-test")
    except ResumeBuildError as exc:
        sys.stdout.flush()
        print(f"error: {exc}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
