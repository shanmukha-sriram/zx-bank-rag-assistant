from dataclasses import dataclass
import re


@dataclass
class Section:
    heading: str
    level: int
    heading_path: str
    content: str


HEADING_RE = re.compile(r"^(#{1,6})\s+(.*)$")


def parse_sections(text: str) -> list[Section]:
    lines = text.split("\n")
    sections: list[Section] = []
    stack: list[tuple[int, str]] = []

    current_heading, current_level, current_lines = "Introduction", 0, []

    def heading_path() -> str:
        return " > ".join(h for _, h in stack) if stack else current_heading

    def flush():
        if current_lines and "\n".join(current_lines).strip():
            sections.append(Section(current_heading, current_level, heading_path(), "\n".join(current_lines).strip()))

    for line in lines:
        match = HEADING_RE.match(line)
        if match:
            flush()
            current_lines = []
            level, heading = len(match.group(1)), match.group(2).strip()
            stack = [(lvl, h) for lvl, h in stack if lvl < level] + [(level, heading)]
            current_heading, current_level = heading, level
        else:
            current_lines.append(line)

    flush()
    return sections