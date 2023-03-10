#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
from pathlib import Path
import os
import logging

from .logger import init_logger

init_logger()

log = logging.getLogger(__name__)


class Settings:
    timezone: str = "America/Denver"
    template_dir: Path = Path(__file__).parent / "templates"
    out_dir: Path = Path(os.getenv("OUTDIR", Path(__file__).parent.parent / "output"))
    data: dict = {}

    def __init__(self):
        datafile = os.getenv("DATAFILE", "")
        if datafile:
            datafile = Path(datafile)
            if datafile.exists():
                self.data = json.loads(datafile.read_text())
            else:
                log.info("Creating data file: %s", datafile)
                datafile.parent.mkdir(mode=0o700, exist_ok=True)
                datafile.write_text("{}")
        else:
            log.error("No DATAFILE env var exists")
            raise ValueError("use DATAFILE env var")


settings = Settings()
