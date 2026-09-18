import json
from dotenv import load_dotenv
from app.evaluation.runner import run_evaluation


def main():
    load_dotenv()
    print(json.dumps(run_evaluation(), indent=2))


if __name__ == "__main__":
    main()