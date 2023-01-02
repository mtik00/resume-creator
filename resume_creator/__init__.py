#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import logging

from .settings import settings
from .markdown import create_markdown

log = logging.getLogger(__name__)


def main():
    log.debug(settings.data)
    create_markdown()


if __name__ == "__main__":
    main()
