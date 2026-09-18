import sys
from dotenv import load_dotenv

from app.core.exceptions import RAGException
from app.rag.pipeline import answer_question


def main():
    load_dotenv()
    if len(sys.argv) < 2:
        print('Usage: python -m scripts.ask "your question"')
        return

    try:
        result = answer_question(sys.argv[1])
    except RAGException as e:
        print(f"\nError: {e}")
        return

    print("\nAnswer:\n")
    print(result["answer"])

    if result.get("abstained"):
        return

    print("\nSources:")
    for i, s in enumerate(result["sources"], start=1):
        print(f"[{i}] {s['source']} — {s['section']}")

    if result.get("citation_warnings"):
        print("\n⚠ Citation warnings:")
        for w in result["citation_warnings"]:
            print(f" - {w}")


if __name__ == "__main__":
    main()