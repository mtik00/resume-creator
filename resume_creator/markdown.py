#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
from pathlib import Path

import jinja2

from .settings import settings

log = logging.getLogger(__name__)


def create_markdown(output_file: Path = settings.out_dir / "resume.md"):
    templateLoader = jinja2.FileSystemLoader(searchpath=settings.template_dir)
    templateEnv = jinja2.Environment(loader=templateLoader)
    template = templateEnv.get_template("resume.md.j2")
    outputText = template.render(**settings.data)
    # log.info("rendered markdown:\n%s", outputText)

    output_file.write_text(outputText)
