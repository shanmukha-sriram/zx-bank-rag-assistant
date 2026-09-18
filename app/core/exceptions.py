class RAGError(Exception):
    """Base exception for the RAG application."""
    pass

class GenerationError(RAGError):
    pass