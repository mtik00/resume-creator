#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import logging

from .markdown import create_markdown
from .pdf import create_pdf
from .text import create_text

log = logging.getLogger(__name__)


def main():
    create_markdown()
    create_pdf()
    create_text()


if __name__ == "__main__":
    main()
