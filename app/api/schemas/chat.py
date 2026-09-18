# from pydantic import BaseModel


# class ChatRequest(BaseModel):
#     question: str


# class Citation(BaseModel):
#     source: str
#     section: str


# class ChatResponse(BaseModel):
#     answer: str
#     citations: list[Citation]
#     abstained: bool

from pydantic import BaseModel
from typing import Any


class ChatRequest(BaseModel):
    question: str
    history: list[dict[str, Any]] = []  # Default to empty list for backward compatibility


class Citation(BaseModel):
    source: str
    section: str


class ChatResponse(BaseModel):
    answer: str
    citations: list[Citation]
    abstained: bool