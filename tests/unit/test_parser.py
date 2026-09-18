from app.ingestion.parser import parse_sections

SAMPLE_MD = """# House Loan

Some intro text.

## Eligibility

Applicants must be over 21.
"""


def test_parse_sections_extracts_headings():
    headings = [s.heading for s in parse_sections(SAMPLE_MD)]
    assert "House Loan" in headings and "Eligibility" in headings


def test_heading_path_reflects_hierarchy():
    sections = parse_sections(SAMPLE_MD)
    eligibility = next(s for s in sections if s.heading == "Eligibility")
    assert eligibility.heading_path == "House Loan > Eligibility"


def test_no_headings_returns_single_intro_section():
    sections = parse_sections("Just plain text, no headings.")
    assert len(sections) == 1 and sections[0].heading == "Introduction"