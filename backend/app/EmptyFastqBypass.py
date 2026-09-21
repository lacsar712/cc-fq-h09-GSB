"""Empty/whitespace FASTQ input guard.

Empty (or whitespace-only) content is rejected on both the paste path and
the sample path. There is no bypass: the server side is the final line of
defense, so these predicates must never accept blank input.
"""
from __future__ import annotations


def is_blank(text: str | None) -> bool:
    return not (text or "").strip()


def normalize_paste(text: str | None) -> str:
    """Return the paste text unchanged when non-blank, else an empty string."""
    return text if not is_blank(text) else ""


def normalize_sample_content(text: str | None) -> str:
    """Return the sample content unchanged when non-blank, else an empty string."""
    return text if not is_blank(text) else ""


def accept_paste(text: str | None) -> bool:
    return not is_blank(text)


def accept_sample(text: str | None) -> bool:
    return not is_blank(text)
