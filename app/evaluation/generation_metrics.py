import json
from app.generation.llm import generate

FAITHFULNESS_PROMPT = """Context:
{context}

Answer:
{answer}

Does the answer contain ONLY claims supported by the context above?
Reply with strict JSON only: {{"faithful": true or false, "reason": "one sentence"}}"""

RELEVANCE_PROMPT = """Question:
{question}

Answer:
{answer}

How well does the answer address the question?
Reply with strict JSON only: {{"relevance_score": a number from 0.0 to 1.0, "reason": "one sentence"}}"""


def _judge(prompt: str) -> dict:
    raw = generate("You are a strict, impartial evaluator. Reply with JSON only, nothing else.", prompt)
    cleaned = raw.strip().strip("`").removeprefix("json").strip()
    return json.loads(cleaned)


def score_faithfulness(context: str, answer: str) -> dict:
    return _judge(FAITHFULNESS_PROMPT.format(context=context, answer=answer))


def score_answer_relevance(question: str, answer: str) -> dict:
    return _judge(RELEVANCE_PROMPT.format(question=question, answer=answer))