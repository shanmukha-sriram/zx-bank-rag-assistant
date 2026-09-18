"""Milestone 1 / Phase 0 — Dataset inspection.

Run: python scripts/inspect_dataset.py
"""
from pathlib import Path
import re

DATA_DIR = Path(__file__).resolve().parent.parent / "data" / "raw" / "zx_bank"


def find_markdown_files(data_dir: Path) -> list[Path]:
    return sorted(data_dir.rglob("*.md"))


def count_headings(text: str) -> int:
    return len(re.findall(r"^#{1,6}\s+.+", text, flags=re.MULTILINE))


def inspect() -> None:
    files = find_markdown_files(DATA_DIR)

    if not files:
        print(f"No markdown files found in {DATA_DIR}")
        print("Add your ZX Bank .md files there and re-run this script.")
        return

    word_counts, char_counts, heading_counts = [], [], []

    print(f"Found {len(files)} markdown document(s) in {DATA_DIR}\n")
    print(f"{'File':45} {'Words':>8} {'Chars':>8} {'Headings':>9}")
    print("-" * 75)

    for f in files:
        text = f.read_text(encoding="utf-8", errors="ignore")
        words, chars, headings = len(text.split()), len(text), count_headings(text)
        word_counts.append(words)
        char_counts.append(chars)
        heading_counts.append(headings)
        print(f"{f.name:45} {words:>8} {chars:>8} {headings:>9}")

    print("-" * 75)
    print(f"Total documents:      {len(files)}")
    print(f"Total words:          {sum(word_counts)}")
    print(f"Average doc length:   {sum(word_counts) / len(files):.1f} words")
    print(f"Shortest document:    {min(word_counts)} words")
    print(f"Longest document:     {max(word_counts)} words")
    print(f"Average headings/doc: {sum(heading_counts) / len(files):.1f}")


if __name__ == "__main__":
    inspect()