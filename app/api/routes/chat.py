# from fastapi import APIRouter
# from app.api.schemas.chat import ChatRequest, ChatResponse, Citation
# from app.rag.pipeline import answer_question

# router = APIRouter()


# @router.post("/chat", response_model=ChatResponse)
# def chat(request: ChatRequest):
#     result = answer_question(request.question)
#     return ChatResponse(
#         answer=result["answer"],
#         citations=[Citation(**s) for s in result["sources"]],
#         abstained=result["abstained"],
#     )

from fastapi import APIRouter
from app.api.schemas.chat import ChatRequest, ChatResponse, Citation
from app.rag.pipeline import answer_question

router = APIRouter()


@router.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    # Pass both question and history to pipeline
    result = answer_question(
        question=request.question,
        history=request.history
    )
    return ChatResponse(
        answer=result["answer"],
        citations=[Citation(**s) for s in result["sources"]],
        abstained=result["abstained"],
    )