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
SECTION_BREAK = 0.5 * inch
VISIBLE_WIDTH = width - MARGIN


def create_pdf():
    fonts_dir = Path(__file__).parent / "fonts"
    pdfmetrics.registerFont(TTFont("Garamond", fonts_dir / "EBGaramond-Regular.ttf"))
    pdfmetrics.registerFont(
        TTFont("Garamond Bold", fonts_dir / "EBGaramond-SemiBold.ttf")
    )
    pdfmetrics.registerFont(
        TTFont("Garamond Medium Italic", fonts_dir / "EBGaramond-Italic.ttf")
    )

    c = canvas.Canvas("resume.pdf", bottomup=0, pagesize=letter)

    y = MARGIN
    c.setFont("Garamond Bold", 24)
    c.drawString(MARGIN, y, settings.data["name"])

    c.setFont("Garamond", 16)
    data = settings.data
    line = f"{data['email']} \u2022 {data['phone']} \u2022 {data['location']}"
    y += 0.3 * inch
    c.drawString(MARGIN, y, line)

    y += 0.15 * inch
    c.setLineWidth(1)
    c.line(MARGIN, y, VISIBLE_WIDTH, y)

    y += 0.25 * inch

    y = experience(y, c) + SECTION_BREAK
    y = education(y, c) + SECTION_BREAK
    y = skills_and_interests(y, c) + SECTION_BREAK

    c.save()


def section_header(y: int, c: canvas.Canvas, text: str):
    c.setFont("Garamond Bold", 12)
    c.drawString(MARGIN, y, text)

    y += 0.15 * inch
    c.line(MARGIN, y, VISIBLE_WIDTH, y)

    return y


def skills_and_interests(y: int, c: canvas.Canvas) -> int:
    y = section_header(y, c, "SKILLS & INTERESTS")
    skills = "Skills: " + ", ".join(settings.data["skills"])
    interests = "Interests: " + ", ".join(settings.data["interests"])

    y += 0.25 * inch
    stylesheet = getSampleStyleSheet()
    normalStyle = stylesheet["Normal"]
    style = ParagraphStyle(
        "bullets",
        normalStyle,
        bulletIndent=0,
        leftIndent=20,
        fontName="Garamond",
        fontSize=12,
    )
    p = Paragraph(text=skills, style=style, bulletText="\u2022")
    p.wrapOn(c, VISIBLE_WIDTH - 0.5 * inch, 0)
    p.drawOn(c, MARGIN, y - p.height + 0.1 * inch)
    y += p.height + 0.05 * inch

    p = Paragraph(text=interests, style=style, bulletText="\u2022")
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
        stylesheet = getSampleStyleSheet()
        normalStyle = stylesheet["Normal"]
        style = ParagraphStyle(
            "bullets",
            normalStyle,
            bulletIndent=0,
            leftIndent=20,
            fontName="Garamond",
            fontSize=12,
        )
        for item in job["responsibilities"]:
            p = Paragraph(text=item, style=style, bulletText="\u2022")
            p.wrapOn(c, VISIBLE_WIDTH - 0.5 * inch, 0)
            p.drawOn(c, MARGIN, y - p.height + 0.1 * inch)
            y += p.height + 0.05 * inch

        # Remove the last paragraph height to preserve some space between experiences.
        y -= p.height

    return y


if __name__ == "__main__":
    create_pdf()
