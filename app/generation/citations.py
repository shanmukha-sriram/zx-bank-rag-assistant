import re

CITATION_RE = re.compile(r"\[(\d+)\]")


def validate_citations(answer: str, num_sources: int) -> list[str]:
    warnings = []
    cited = {int(n) for n in CITATION_RE.findall(answer)}

    invalid = {i for i in cited if i < 1 or i > num_sources}
    if invalid:
        warnings.append(f"Answer cites source(s) {sorted(invalid)} that weren't in the provided context.")

    if not cited and num_sources > 0:
        warnings.append("Answer has no citation markers even though sources were provided.")

    return warnings