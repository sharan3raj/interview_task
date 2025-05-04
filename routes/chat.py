from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from services.chat_service import ChatService
from core.config import settings

router = APIRouter()
chat_service = ChatService()

class ChatRequest(BaseModel):
    question: str

class ChatResponse(BaseModel):
    answer: str
    sources: list[str]

@router.post("/", response_model=ChatResponse)
async def chat(request: ChatRequest):
    try:
        result = chat_service.get_response(request.question)
        return ChatResponse(
            answer=result["answer"],
            sources=[doc.metadata.get("source", "Unknown") for doc in result["source_documents"]]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 