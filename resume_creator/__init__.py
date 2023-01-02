#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import logging

from .settings import settings

log = logging.getLogger(__name__)


def main():
    log.debug(settings.data)


if __name__ == "__main__":
    main()
