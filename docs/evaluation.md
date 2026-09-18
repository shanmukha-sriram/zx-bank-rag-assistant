# Evaluation

## Golden Dataset
`data/evaluation/golden_dataset.json` — hand-authored question/answer pairs referencing real chunk IDs (via `scripts/list_chunks.py`), covering descriptive, procedural, comparative, boolean, and temporal question types, plus deliberately unsupported questions (empty `relevant_chunks`) to test abstention.

Current size: `<fill in — target 50-200, growing over time>`

## Retrieval Metrics — `app/evaluation/retrieval_metrics.py`
- **Recall@K** — did a truly relevant chunk make it into the top K retrieved?
- **Precision@K** — of the K retrieved chunks, how many were actually relevant?
- **MRR** — how high up did the first relevant chunk rank?

## Generation Metrics — `app/evaluation/generation_metrics.py`
Custom LLM-as-judge scoring (not RAGAS — see `docs/decisions.md` for why):
- **Faithfulness** — does the answer only make claims the context actually supports?
- **Answer Relevance** — does the answer actually address the question asked?

## Abstention Accuracy
For golden-set questions with no relevant chunks (deliberately unsupported), we measure whether the system correctly abstained rather than hallucinating an answer.

## Current Baseline
Output of `python -m scripts.evaluate`. Replace with your real numbers and update whenever the pipeline changes meaningfully:

```json
{
  "num_answerable_examples": 9,
  "num_unsupported_examples": 3,
  "recall_at_k": 0.7037037037037037,
  "precision_at_k": 0.15555555555555556,
  "mrr": 0.5444444444444445,
  "faithfulness": 0.7777777777777778,
  "avg_answer_relevance": 0.8288888888888889,
  "abstention_accuracy": 0.0
}
```

## Quality Thresholds
The CI quality gate (`scripts/check_quality_gate.py`) enforces minimums set just below this baseline, so regressions fail a PR rather than shipping silently:

| Metric | Threshold | Basis |
|---|---|---|
| `recall_at_k` | `0.5` | Calibrated to baseline |
| `mrr` | `0.5` | Calibrated to baseline |
| `faithfulness` | `0.5` | Calibrated to baseline |

These are **not** invented numbers — measure first, threshold second.
