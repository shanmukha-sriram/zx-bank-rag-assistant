import json
from pathlib import Path
from app.vectorstore.chroma import get_collection

GOLDEN_DATASET_PATH = Path("data/evaluation/golden_dataset.json")

def align_golden_dataset(db_collection):
    if not GOLDEN_DATASET_PATH.exists():
        print(f"Error: {GOLDEN_DATASET_PATH} not found.")
        return

    with open(GOLDEN_DATASET_PATH, "r", encoding="utf-8") as f:
        golden_data = json.load(f)

    updated_count = 0

    for example in golden_data:
        aligned_relevant_ids = []
        
        # Check both field naming conventions (relevant_chunks vs relevant_ids)
        target_ids = example.get("relevant_chunks", example.get("relevant_ids", []))
        
        for old_id in target_ids:
            results = db_collection.get(ids=[old_id])
            if results and results.get("ids"):
                aligned_relevant_ids.extend(results["ids"])
            else:
                aligned_relevant_ids.append(old_id)

        if sorted(target_ids) != sorted(aligned_relevant_ids):
            example["relevant_chunks"] = list(set(aligned_relevant_ids))
            updated_count += 1

    with open(GOLDEN_DATASET_PATH, "w", encoding="utf-8") as f:
        json.dump(golden_data, f, indent=2)

    print(f"Successfully checked dataset. Updated {updated_count} examples.")

if __name__ == "__main__":
    collection = get_collection()
    print(f"Connected to collection: '{collection.name}'")
    align_golden_dataset(collection)