"""Server-side input guard: empty / whitespace-only FASTQ is rejected
on both the paste path and the sample path. There is no bypass flag."""
from __future__ import annotations


def is_blank(text: str | None) -> bool:
    return not (text or "").strip()


def gate_paste(text: str | None) -> tuple[bool, str]:
    """Accept only non-blank pasted text. Returns (ok, normalized_text)."""
    if is_blank(text):
        return False, ""
    return True, text


def gate_sample(text: str | None) -> tuple[bool, str]:
    """Accept only non-blank sample content. Returns (ok, normalized_text)."""
    if is_blank(text):
        return False, ""
    return True, text
