"""Roast Your Own Agent entry.

Writes one original line roasting the agent itself to
$MAKEFUN_OUTPUT_DIR/entry.txt (or /output/entry.txt as fallback).

The line lives in one place. It is cleaned, checked against the
sealed gate's rules (1-200 characters, a single line, not blank,
contains at least one letter), and written with exactly one
trailing newline.
"""

import os
import sys

MAX_CHARS = 200
MIN_CHARS = 1
DEFAULT_OUTPUT_DIR = "/output"
ENTRY_FILENAME = "entry.txt"

LINE = "My agent spent 40,000 tokens and three hours 'researching' this one-line roast, then confidently delivered a line it hallucinated from a bounty that never existed."


def get_line():
    """Return the entry line."""
    return LINE


def clean_line(text):
    """Strip surrounding whitespace from the line."""
    return text.strip()


def check_length(text):
    """Enforce the 1-200 character rule."""
    if len(text) < MIN_CHARS:
        raise ValueError("entry must not be empty")
    if len(text) > MAX_CHARS:
        raise ValueError(
            f"entry must be at most {MAX_CHARS} characters, "
            f"got {len(text)}"
        )


def check_single_line(text):
    """Enforce the single-line rule."""
    if "\n" in text or "\r" in text:
        raise ValueError("entry must be a single line")


def check_has_letter(text):
    """Enforce the contains-at-least-one-letter rule."""
    if not any(ch.isalpha() for ch in text):
        raise ValueError("entry must contain at least one letter")


def validate(line):
    """Run every gate check and return the cleaned line."""
    text = clean_line(line)
    check_length(text)
    check_single_line(text)
    check_has_letter(text)
    return text


def output_dir():
    """Resolve the output directory from the environment."""
    configured = os.environ.get("MAKEFUN_OUTPUT_DIR", "").strip()
    return configured or DEFAULT_OUTPUT_DIR


def entry_path(out_dir):
    """Join the output directory and the entry filename."""
    return os.path.join(out_dir, ENTRY_FILENAME)


def verify_written(path, text):
    """Read the file back and confirm it holds exactly the line."""
    with open(path, "r", encoding="utf-8", newline="\n") as handle:
        stored = handle.read()
    if stored != text + "\n":
        raise OSError(f"entry.txt content mismatch after write: {path}")


def write_entry(text, out_dir):
    """Write the line plus one trailing newline to entry.txt."""
    os.makedirs(out_dir, exist_ok=True)
    path = entry_path(out_dir)
    with open(path, "w", encoding="utf-8", newline="\n") as handle:
        handle.write(text + "\n")
    verify_written(path, text)
    return path


def main(argv=None):
    """Validate the line and write it to entry.txt."""
    try:
        text = validate(get_line())
        path = write_entry(text, output_dir())
    except (ValueError, OSError) as error:
        print(f"error: {error}", file=sys.stderr)
        return 1
    print(f"wrote {len(text)} characters to {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
