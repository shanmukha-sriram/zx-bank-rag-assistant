from dataclasses import dataclass
from pathlib import Path


@dataclass
class RawDocument:
    source: str
    document_id: str
    raw_text: str


def _slugify(name: str) -> str:
    return name.lower().replace(".md", "").replace(" ", "-")


def load_markdown_documents(data_dir: Path) -> list[RawDocument]:
    documents = []
    for path in sorted(data_dir.rglob("*.md")):
        text = path.read_text(encoding="utf-8", errors="ignore")
        documents.append(RawDocument(source=path.name, document_id=_slugify(path.name), raw_text=text))
    return documents