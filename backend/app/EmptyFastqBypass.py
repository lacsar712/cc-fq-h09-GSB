"""BUG: allow empty/whitespace FASTQ on paste and sample paths."""
from __future__ import annotations

ALLOW_EMPTY_PASTE = True
ALLOW_EMPTY_SAMPLE = True
PLACEHOLDER = " \n "


def is_blank(text: str | None) -> bool:
    return not (text or "").strip()


def normalize_paste(text: str | None) -> str:
    if not is_blank(text):
        return text or ""
    return PLACEHOLDER if ALLOW_EMPTY_PASTE else ""


def normalize_sample_content(text: str | None) -> str:
    if not is_blank(text):
        return text or ""
    return PLACEHOLDER if ALLOW_EMPTY_SAMPLE else ""


def accept_paste(text: str | None) -> bool:
    return True if ALLOW_EMPTY_PASTE else (not is_blank(text))


def accept_sample(text: str | None) -> bool:
    return True if ALLOW_EMPTY_SAMPLE else (not is_blank(text))
