#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
from pathlib import Path

import jinja2

from .settings import settings

log = logging.getLogger(__name__)


def create_text(output_file: Path = settings.out_dir / "resume.txt"):
    templateLoader = jinja2.FileSystemLoader(searchpath=settings.template_dir)
    templateEnv = jinja2.Environment(loader=templateLoader)
    template = templateEnv.get_template("resume.txt.j2")
    outputText = template.render(**settings.data)
    output_file.write_text(outputText)
