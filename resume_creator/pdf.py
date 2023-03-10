#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from pathlib import Path

from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from reportlab.platypus.paragraph import Paragraph

from .settings import settings

width, height = letter

MARGIN = 0.5 * inch
SECTION_BREAK = 0.3 * inch
VISIBLE_WIDTH = width - MARGIN
PARAGRAPH_STYLE = ParagraphStyle(
    "bullets",
    getSampleStyleSheet()["Normal"],
    bulletIndent=0,
    leftIndent=20,
    fontName="Garamond",
    fontSize=12,
)


def create_pdf(output_file: Path = settings.out_dir / "resume.pdf"):
    register_fonts()

    if not output_file.parent.exists():
        output_file.parent.mkdir(parents=True)

    c = canvas.Canvas(str(output_file), bottomup=0, pagesize=letter)

    y = header(c) + 0.15 * inch

    c.setLineWidth(1)
    c.line(MARGIN, y, VISIBLE_WIDTH, y)

    y += 0.25 * inch

    y = experience(y, c) + SECTION_BREAK
    y = education(y, c) + SECTION_BREAK
    y = skills_and_interests(y, c) + SECTION_BREAK

    footer(c)

    c.save()


def header(c: canvas.Canvas) -> int:
    c.setFont("Garamond Bold", 24)
    c.drawString(MARGIN - 0.05 * inch, MARGIN, settings.data["name"])

    c.setFont("Garamond", 16)
    data = settings.data
    line = f"<font name='Courier' size=12>{data['email']}</font> \u00BB {data['phone']} \u00BB {data['location']}"

    y = MARGIN + 0.3 * inch

    p = Paragraph(text=line, style=PARAGRAPH_STYLE)
    p.wrapOn(c, VISIBLE_WIDTH - 0.5 * inch, height)
    p.drawOn(c, MARGIN - 0.28 * inch, y)

    return y


def register_fonts():
    fonts_dir = Path(__file__).parent / "fonts"
    pdfmetrics.registerFont(TTFont("Garamond", fonts_dir / "EBGaramond-Regular.ttf"))
    pdfmetrics.registerFont(
        TTFont("Garamond Bold", fonts_dir / "EBGaramond-SemiBold.ttf")
    )
    pdfmetrics.registerFont(
        TTFont("Garamond Medium Italic", fonts_dir / "EBGaramond-Italic.ttf")
    )


def footer(c: canvas.Canvas):
    line = settings.data["linkedin"]

    c.setFont("Garamond", 12)
    string_width = c.stringWidth(line, "Garamond", 12)

    x = (VISIBLE_WIDTH / 2) - (string_width / 2)
    c.drawString(x, height - MARGIN, line)


def section_header(y: int, c: canvas.Canvas, text: str):
    c.setFont("Garamond Bold", 12)
    c.drawString(MARGIN, y, text)

    y += 0.15 * inch
    c.line(MARGIN, y, VISIBLE_WIDTH, y)

    return y


def skills_and_interests(y: int, c: canvas.Canvas) -> int:
    y = section_header(y, c, "SKILLS & INTERESTS")
    skills = "<font name='Garamond Bold' size=12>Skills:</font> " + ", ".join(
        settings.data["skills"]
    )
    interests = "<font name='Garamond Bold' size=12>Interests:</font> " + ", ".join(
        settings.data["interests"]
    )

    y += 0.25 * inch

    p = Paragraph(text=skills, style=PARAGRAPH_STYLE, bulletText="\u2022")
    p.wrapOn(c, VISIBLE_WIDTH - 0.5 * inch, 0)
    p.drawOn(c, MARGIN, y - p.height + 0.1 * inch)
    y += p.height + 0.05 * inch

    p = Paragraph(text=interests, style=PARAGRAPH_STYLE, bulletText="\u2022")
    p.wrapOn(c, VISIBLE_WIDTH - 0.5 * inch, 0)
    p.drawOn(c, MARGIN, y - p.height + 0.1 * inch)
    y += p.height + 0.05 * inch

    return y


def education(y: int, c: canvas.Canvas) -> int:
    y = section_header(y, c, "EDUCATION")

    y += 0.2 * inch
    for item in settings.data["education"]:
        c.setFont("Garamond Bold", 12)
        c.drawString(MARGIN, y, item["school"])

        string_width = c.stringWidth(item["graduation_date"], "Garamond Bold", 12)
        c.drawString(VISIBLE_WIDTH - string_width, y, item["graduation_date"])

        y += 0.2 * inch
        c.setFont("Garamond Medium Italic", 12)
        c.drawString(MARGIN, y, item["degree"])

        string_width = c.stringWidth(item["location"], "Garamond Medium Italic", 12)
        c.drawString(VISIBLE_WIDTH - string_width, y, item["location"])

        y += 0.4 * inch

    # Remove the last height spacing to preserve some space between experiences.
    y -= 0.4 * inch

    return y


def experience(y: int, c: canvas.Canvas) -> int:
    y = section_header(y, c, "WORK EXPERIENCE")
    y += 0.1 * inch
    for job in settings.data["experiences"]:
        y += 0.2 * inch
        c.setFont("Garamond Bold", 12)
        c.drawString(MARGIN, y, job["company"])

        string_width = c.stringWidth(job["dates"], "Garamond Bold", 12)

        c.drawString(VISIBLE_WIDTH - string_width, y, job["dates"])

        y += 0.2 * inch
        c.setFont("Garamond Medium Italic", 12)
        c.drawString(MARGIN, y, ", ".join(job["titles"]))

        string_width = c.stringWidth(job["location"], "Garamond Medium Italic", 12)
        c.drawString(VISIBLE_WIDTH - string_width, y, job["location"])

        c.setFont("Garamond", 12)
        y += 0.25 * inch

        for item in job["responsibilities"]:
            p = Paragraph(text=item, style=PARAGRAPH_STYLE, bulletText="\u2022")
            p.wrapOn(c, VISIBLE_WIDTH - 0.5 * inch, 0)
            p.drawOn(c, MARGIN, y - p.height + 0.1 * inch)
            y += p.height + 0.05 * inch

        if job["technologies"]:
            technologies = (
                "<font name='Garamond Bold' size=12>Technologies:</font> "
                + ", ".join(job["technologies"])
            )
            p = Paragraph(text=technologies, style=PARAGRAPH_STYLE, bulletText="\u2022")
            p.wrapOn(c, VISIBLE_WIDTH - 0.5 * inch, 0)
            p.drawOn(c, MARGIN, y - p.height + 0.1 * inch)
            y += p.height + 0.05 * inch

        # Remove the last paragraph height to preserve some space between experiences.
        y -= p.height

    return y


if __name__ == "__main__":
    create_pdf()
