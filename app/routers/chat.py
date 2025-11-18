from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
import os
import openai

router = APIRouter()

# التحقق من مفتاح OpenAI
openai.api_key = os.environ.get("OPENAI_API_KEY")
if not openai.api_key:
    raise RuntimeError("OPENAI_API_KEY is not set in environment variables")

class ChatRequest(BaseModel):
    message: str
    fingerprint: Optional[str] = None

class ChatResponse(BaseModel):
    reply: str

@router.post("/chat", response_model=ChatResponse)
async def chat_endpoint(req: ChatRequest):
    fp = req.fingerprint or "default"
    try:
        response = openai.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "أنت مساعد ذكي، ترد باختصار وبوضوح."},
                {"role": "user", "content": f"Fingerprint: {fp}\nMessage: {req.message}"}
            ],
            temperature=0.7
        )
        reply_text = response.choices[0].message.content.strip()
        return ChatResponse(reply=reply_text)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"خطأ في OpenAI API: {e}")
