import json
from pathlib import Path
from dataclasses import dataclass

GOLDEN_DATASET_PATH = Path("data/evaluation/golden_dataset.json")


@dataclass
class GoldenExample:
    question: str
    ground_truth_answer: str
    relevant_documents: list[str]
    relevant_chunks: list[str]


def load_golden_dataset() -> list[GoldenExample]:
    raw = json.loads(GOLDEN_DATASET_PATH.read_text(encoding="utf-8"))
    return [GoldenExample(**item) for item in raw]