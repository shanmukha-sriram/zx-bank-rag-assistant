# from pathlib import Path

# PROMPTS_DIR = Path(__file__).resolve().parent.parent.parent / "prompts" / "v1"


# def load_system_prompt() -> str:
#     return (PROMPTS_DIR / "system.txt").read_text(encoding="utf-8")


# def build_context(chunks: list[dict]) -> str:
#     lines = []
#     for i, c in enumerate(chunks, start=1):
#         lines.append(f"[{i}] Source: {c['metadata']['source']} | Section: {c['metadata']['section']}")
#         lines.append(c["text"])
#         lines.append("")
#     return "\n".join(lines)


# def build_user_prompt(question: str, chunks: list[dict]) -> str:
#     template = (PROMPTS_DIR / "answer.txt").read_text(encoding="utf-8")
#     return template.format(context=build_context(chunks), question=question)

from pathlib import Path

PROMPTS_DIR = Path(__file__).resolve().parent.parent.parent / "prompts" / "v1"


def load_system_prompt() -> str:
    return (PROMPTS_DIR / "system.txt").read_text(encoding="utf-8")


def build_context(chunks: list[dict]) -> str:
    lines = []
    for i, c in enumerate(chunks, start=1):
        lines.append(f"[{i}] Source: {c['metadata']['source']} | Section: {c['metadata']['section']}")
        lines.append(c["text"])
        lines.append("")
    return "\n".join(lines)


def format_history(history: list[dict]) -> str:
    if not history:
        return "No prior context."
    lines = []
    for msg in history[-4:]:  # Take last 4 turns for context
        role = "User" if msg.get("role") == "user" else "Assistant"
        lines.append(f"{role}: {msg.get('content', '')}")
    return "\n".join(lines)


def build_user_prompt(question: str, chunks: list[dict], history: list[dict] = None) -> str:
    template = (PROMPTS_DIR / "answer.txt").read_text(encoding="utf-8")
    context_str = build_context(chunks)
    history_str = format_history(history or [])
    
    # Checks if answer.txt expects {history}; falls back to question + context if template isn't updated
    if "{history}" in template:
        return template.format(history=history_str, context=context_str, question=question)
    return template.format(context=context_str, question=f"Previous Conversation:\n{history_str}\n\nUser Question: {question}")