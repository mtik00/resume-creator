#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import logging

from .markdown import create_markdown
from .pdf import create_pdf
from .settings import settings
from .text import create_text

log = logging.getLogger(__name__)


def main():
    partial_path = f"{settings.data['name']} Resume"

    settings.out_dir.mkdir(parents=True, exist_ok=True)

    path = settings.out_dir / f"{partial_path}.md"
    create_markdown(path)
    log.info("%s created", path)

    path = settings.out_dir / f"{partial_path}.pdf"
    create_pdf(path)
    log.info("%s created", path)

    path = settings.out_dir / f"{partial_path}.txt"
    create_text(path)
    log.info("%s created", path)


if __name__ == "__main__":
    main()
