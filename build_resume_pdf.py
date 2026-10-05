from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any

from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import (
    KeepTogether,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
)


def clean_filename(value: str) -> str:
    value = re.sub(r"[^A-Za-z0-9._-]+", "_", value).strip("_.")
    return value[:120] or "tailored_resume"


def bullet(text: str, style: ParagraphStyle) -> Paragraph:
    return Paragraph(f"• {text}", style)


def build(data: dict[str, Any], output: Path) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    styles = getSampleStyleSheet()
    name = ParagraphStyle("name", parent=styles["Heading1"], fontSize=17, leading=20, spaceAfter=2, alignment=TA_LEFT)
    headline = ParagraphStyle("headline", parent=styles["Normal"], fontSize=9.5, leading=12, spaceAfter=5)
    contact = ParagraphStyle("contact", parent=styles["Normal"], fontSize=8.5, leading=11, spaceAfter=7)
    section = ParagraphStyle("section", parent=styles["Heading2"], fontSize=10.5, leading=13, spaceBefore=5, spaceAfter=3)
    body = ParagraphStyle("body", parent=styles["Normal"], fontSize=8.6, leading=11, spaceAfter=3)
    small = ParagraphStyle("small", parent=body, fontSize=8, leading=10)
    exp_head = ParagraphStyle("exphead", parent=body, fontSize=9, leading=11, spaceBefore=2, spaceAfter=1)
    story: list[Any] = []

    story.append(Paragraph(data.get("name", "Karina Rohra"), name))
    story.append(Paragraph(data.get("headline", ""), headline))
    story.append(Paragraph(data.get("contact", ""), contact))

    summary = data.get("summary")
    if summary:
        story.append(Paragraph("PROFESSIONAL SUMMARY", section))
        story.append(Paragraph(summary, body))

    skills = data.get("skills", {})
    if skills:
        story.append(Paragraph("CORE SKILLS", section))
        for label, value in skills.items():
            story.append(Paragraph(f"<b>{label}:</b> {value}", body))

    experiences = data.get("experience", [])
    if experiences:
        story.append(Paragraph("PROFESSIONAL EXPERIENCE", section))
        for exp in experiences:
            title = exp.get("title", "")
            company = exp.get("company", "")
            dates = exp.get("dates", "")
            story.append(KeepTogether([Paragraph(f"<b>{title}</b> | {company} | {dates}", exp_head)]))
            for b in exp.get("bullets", []):
                story.append(bullet(b, body))

    ai = data.get("ai_experience", [])
    if ai:
        story.append(Paragraph("AI-ASSISTED DIGITAL MARKETING EXPERIENCE", section))
        for b in ai:
            story.append(bullet(b, body))

    education = data.get("education", [])
    if education:
        story.append(Paragraph("EDUCATION", section))
        for e in education:
            story.append(Paragraph(f"<b>{e.get('degree','')}</b> | {e.get('institution','')} | {e.get('dates','')}", body))
            if e.get("detail"):
                story.append(Paragraph(e["detail"], small))

    certs = data.get("certifications", [])
    if certs:
        story.append(Paragraph("CERTIFICATIONS & TRAINING", section))
        for c in certs:
            story.append(bullet(c, body))

    portfolio = data.get("portfolio")
    if portfolio:
        story.append(Paragraph("PORTFOLIO", section))
        story.append(Paragraph(portfolio, small))

    doc = SimpleDocTemplate(
        str(output), pagesize=A4, rightMargin=14*mm, leftMargin=14*mm,
        topMargin=12*mm, bottomMargin=12*mm,
        title=f"{data.get('name','Karina Rohra')} - Tailored Resume",
        author=data.get("name", "Karina Rohra"),
    )
    doc.build(story)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    data = json.loads(args.input.read_text(encoding="utf-8"))
    build(data, args.output)
    print(args.output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
