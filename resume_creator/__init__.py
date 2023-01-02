#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import logging

from .settings import settings
from .markdown import create_markdown
from .pdf import create_pdf


log = logging.getLogger(__name__)


def main():
    log.debug(settings.data)
    create_markdown()
    create_pdf()


if __name__ == "__main__":
    main()
