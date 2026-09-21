"""Guard tests: empty / whitespace-only FASTQ is rejected on every path."""

import pytest

from app.EmptyFastqBypass import (
    accept_paste,
    accept_sample,
    is_blank,
    normalize_paste,
    normalize_sample_content,
)
from app.EmptyInputGate import gate_paste, gate_sample


BLANK_INPUTS = ["", "   ", "\t\n\r", " \n\t ", None]
VALID_INPUT = "@SEQ1\nACGT\n+\nIIII\n"


@pytest.mark.parametrize("text", BLANK_INPUTS)
def test_paste_rejects_blank(text):
    assert accept_paste(text) is False


@pytest.mark.parametrize("text", BLANK_INPUTS)
def test_sample_rejects_blank(text):
    assert accept_sample(text) is False


@pytest.mark.parametrize("text", BLANK_INPUTS)
def test_normalize_blank_becomes_empty(text):
    assert normalize_paste(text) == ""
    assert normalize_sample_content(text) == ""


def test_valid_paste_accepted_and_unchanged():
    assert accept_paste(VALID_INPUT) is True
    assert normalize_paste(VALID_INPUT) == VALID_INPUT


def test_valid_sample_accepted_and_unchanged():
    assert accept_sample(VALID_INPUT) is True
    assert normalize_sample_content(VALID_INPUT) == VALID_INPUT


def test_is_blank():
    assert is_blank("") is True
    assert is_blank("  \n ") is True
    assert is_blank("x") is False


@pytest.mark.parametrize("text", ["", " \n ", None])
def test_gate_paste_blocks_blank(text):
    ok, normalized = gate_paste(text)
    assert ok is False
    assert normalized == ""


@pytest.mark.parametrize("text", ["", " \n ", None])
def test_gate_sample_blocks_blank(text):
    ok, normalized = gate_sample(text)
    assert ok is False
    assert normalized == ""


def test_gate_passes_valid_text():
    assert gate_paste(VALID_INPUT) == (True, VALID_INPUT)
    assert gate_sample(VALID_INPUT) == (True, VALID_INPUT)
