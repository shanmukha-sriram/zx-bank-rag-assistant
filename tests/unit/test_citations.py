from app.generation.citations import validate_citations


def test_valid_citations_produce_no_warnings():
    assert validate_citations("Must be 21. [1] Needs proof. [2]", num_sources=2) == []


def test_out_of_range_citation_is_flagged():
    warnings = validate_citations("Must be 21. [3]", num_sources=2)
    assert len(warnings) == 1


def test_missing_citations_are_flagged():
    warnings = validate_citations("Must be 21.", num_sources=2)
    assert len(warnings) == 1