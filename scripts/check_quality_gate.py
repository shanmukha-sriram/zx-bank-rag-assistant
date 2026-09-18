import sys
import json
from dotenv import load_dotenv
from app.evaluation.runner import run_evaluation

# Minimum acceptable quality thresholds for your RAG system
THRESHOLDS = {
    "recall_at_k": 0.50,
    "mrr": 0.50,
    "faithfulness": 0.50,
    "abstention_accuracy": 0.50
}

def main():
    load_dotenv()
    print("Running evaluation suite...")
    results = run_evaluation()
    print(json.dumps(results, indent=2))

    failures = []
    for metric, minimum in THRESHOLDS.items():
        val = results.get(metric)
        if val is None or val < minimum:
            failures.append(f"{metric}={val} is below minimum {minimum}")

    if failures:
        print("\n❌ Quality gate FAILED:")
        print("\n".join(f" - {f}" for f in failures))
        sys.exit(1)

    print("\n✅ Quality gate passed.")

if __name__ == "__main__":
    main()