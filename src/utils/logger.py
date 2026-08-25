"""Structured logging utility.

Implements docs/11-Framework-Architecture.md §23 (Logging Strategy):
supplementary, structured execution logging for fixture setup/teardown
visibility (especially account lifecycle, given its shared-environment risk
profile) and test-step context on failure — not a replacement for pytest's
own output.

Generic and AUT-agnostic, per docs/11 §22's utility-scope rule: this module
knows nothing about Automation Exercise; it only formats and emits messages.
"""

from __future__ import annotations

import logging
import os

_CONFIGURED = False


def _configure_root_once() -> None:
    global _CONFIGURED
    if _CONFIGURED:
        return
    level_name = os.getenv("LOG_LEVEL", "INFO").upper()
    level = getattr(logging, level_name, logging.INFO)
    logging.basicConfig(
        level=level,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    _CONFIGURED = True


def get_logger(name: str) -> logging.Logger:
    """Return a module-scoped logger, configuring the root handler on first use."""
    _configure_root_once()
    return logging.getLogger(name)
