from dataclasses import dataclass
import re
from app.ingestion.parser import Section

@dataclass
class Chunk:
    chunk_id: str
    document_id: str
    source: str
    section: str
    heading_path: str
    text: str

def _slugify(text: str) -> str:
    # Clean special characters (dashes, quotes, punctuation) and normalize to lowercase
    text = re.sub(r"[^\w\s-]", "", text).strip().lower()
    return re.sub(r"[-\s]+", "-", text)[:40].strip("-")

def chunk_document(
    document_id: str,
    source: str,
    sections: list[Section],
    chunk_size: int = 600,
    overlap: int = 100,
) -> list[Chunk]:
    chunks: list[Chunk] = []
    chunk_counter = 0  # Global counter per document ensures 100% unique IDs

    for section in sections:
        words = section.content.split()
        if len(words) <= chunk_size:
            chunk_counter += 1
            chunks.append(_make_chunk(document_id, source, section, words, chunk_counter))
            continue
        
        start = 0
        while start < len(words):
            end = min(start + chunk_size, len(words))
            chunk_counter += 1
            chunks.append(_make_chunk(document_id, source, section, words[start:end], chunk_counter))
            if end == len(words):
                break
            start = end - overlap

    return chunks

def _make_chunk(document_id: str, source: str, section: Section, words: list[str], idx: int) -> Chunk:
    section_slug = _slugify(section.heading) or "sec"
    return Chunk(
        chunk_id=f"{document_id}-{section_slug}-{idx:03d}",
        document_id=document_id,
        source=source,
        section=section.heading,
        heading_path=section.heading_path,
        text=" ".join(words),
    )