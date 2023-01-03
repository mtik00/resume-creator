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


def create_pdf():
    fonts_dir = Path(__file__).parent / "fonts"
    pdfmetrics.registerFont(TTFont("Garamond", fonts_dir / "EBGaramond-Regular.ttf"))
    pdfmetrics.registerFont(
        TTFont("Garamond Bold", fonts_dir / "EBGaramond-SemiBold.ttf")
    )
    pdfmetrics.registerFont(
        TTFont("Garamond Medium Italic", fonts_dir / "EBGaramond-Italic.ttf")
    )

    c = canvas.Canvas("resume.pdf", bottomup=0, pagesize=letter, cropMarks=True)

    y = -0.75 * inch
    c.translate(0, y)
    c.setFont("Garamond Bold", 24)
    c.drawString(0, 0, settings.data["name"])

    c.setFont("Garamond", 16)
    data = settings.data
    line = f"{data['email']} \u2022 {data['phone']} \u2022 {data['location']}"
    y += 1.0 * inch
    c.drawString(0.05 * inch, y, line)

    y += 0.15 * inch
    c.setLineWidth(1)
    c.line(0 * inch, y, width, y)

    y += 0.25 * inch

    y = section_header(y, c, "WORK EXPERIENCE")
    # c.setFont("Garamond Bold", 12)
    # c.drawString(0.05 * inch, y, "WORK EXPERIENCE")

    y += 0.15 * inch
    c.line(0 * inch, y, width, y)

    y = experience(y, c)

    c.save()


def section_header(y: int, c: canvas.Canvas, text: str):
    c.setFont("Garamond Bold", 12)
    c.drawString(0.05 * inch, y, "WORK EXPERIENCE")

    y += 0.15 * inch
    c.line(0 * inch, y, width, y)

    return y


def experience(y: int, c: canvas.Canvas) -> int:
    x = 0.05 * inch
    y += 0.1 * inch
    for job in settings.data["experiences"]:
        y += 0.2 * inch
        c.setFont("Garamond Bold", 12)
        c.drawString(x, y, job["company"])

        string_width = c.stringWidth(job["dates"], "Garamond Bold", 12)

        c.drawString(width - string_width, y, job["dates"])

        y += 0.2 * inch
        c.setFont("Garamond Medium Italic", 12)
        c.drawString(x, y, ", ".join(job["titles"]))

        string_width = c.stringWidth(job["location"], "Garamond Medium Italic", 12)
        c.drawString(width - string_width, y, job["location"])

        c.setFont("Garamond", 12)
        y += 0.25 * inch
        stylesheet = getSampleStyleSheet()
        normalStyle = stylesheet["Normal"]
        style = ParagraphStyle(
            "bullets",
            normalStyle,
            bulletIndent=10,
            leftIndent=20,
            fontName="Garamond",
            fontSize=12,
        )
        for item in job["responsibilities"]:
            p = Paragraph(text=item, style=style, bulletText="\u2022")
            p.wrapOn(c, width - 0.5 * inch, 0)
            p.drawOn(c, x, y - p.height + 0.1 * inch)
            y += p.height + 0.05 * inch

        # Remove the last paragraph height to preserve some space between experiences.
        y -= p.height

    return y


if __name__ == "__main__":
    create_pdf()
