import json
from app.evaluation.datasets import load_golden_dataset
from app.evaluation.retrieval_metrics import recall_at_k, precision_at_k, reciprocal_rank
from app.evaluation.generation_metrics import score_faithfulness, score_answer_relevance
from app.retrieval.hybrid_retriever import hybrid_retrieve
from app.retrieval.reranker import rerank
from app.rag.pipeline import answer_question


def run_evaluation(top_k: int = 5) -> dict:
    examples = load_golden_dataset()
    answerable = [e for e in examples if e.relevant_chunks]
    unsupported = [e for e in examples if not e.relevant_chunks]

    recalls, precisions, rr_scores = [], [], []
    faithfulness_scores, relevance_scores = [], []

    for ex in answerable:
        candidates = hybrid_retrieve(ex.question, top_k=20)
        reranked = rerank(ex.question, candidates, top_k=top_k)
        retrieved_ids = [c["chunk_id"] for c in reranked]

        recalls.append(recall_at_k(retrieved_ids, ex.relevant_chunks))
        precisions.append(precision_at_k(retrieved_ids, ex.relevant_chunks))
        rr_scores.append(reciprocal_rank(retrieved_ids, ex.relevant_chunks))

        result = answer_question(ex.question, top_k=top_k)
        if not result["abstained"]:
            context = "\n".join(c["text"] for c in reranked)
            try:
                faithfulness_scores.append(1.0 if score_faithfulness(context, result["answer"])["faithful"] else 0.0)
                relevance_scores.append(score_answer_relevance(ex.question, result["answer"])["relevance_score"])
            except (json.JSONDecodeError, KeyError):
                pass  # judge ignored formatting instructions — skip rather than crash the run

    correct_abstentions = sum(1 for ex in unsupported if answer_question(ex.question, top_k=top_k)["abstained"])
    n = len(answerable) or 1

    return {
        "num_answerable_examples": len(answerable),
        "num_unsupported_examples": len(unsupported),
        "recall_at_k": sum(recalls) / n,
        "precision_at_k": sum(precisions) / n,
        "mrr": sum(rr_scores) / n,
        "faithfulness": sum(faithfulness_scores) / len(faithfulness_scores) if faithfulness_scores else None,
        "avg_answer_relevance": sum(relevance_scores) / len(relevance_scores) if relevance_scores else None,
        "abstention_accuracy": correct_abstentions / len(unsupported) if unsupported else None,
    }