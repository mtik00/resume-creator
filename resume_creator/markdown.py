#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging

import jinja2

from .settings import settings

log = logging.getLogger(__name__)


def create_markdown():
    templateLoader = jinja2.FileSystemLoader(searchpath=settings.template_dir)
    templateEnv = jinja2.Environment(loader=templateLoader)
    template = templateEnv.get_template("resume.md.j2")
    outputText = template.render(**settings.data)
    log.info("rendered markdown:\n%s", outputText)
