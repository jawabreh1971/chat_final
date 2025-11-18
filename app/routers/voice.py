
from fastapi import APIRouter, UploadFile, File, Form, Depends, HTTPException, status
from typing import Optional

from app.auth import get_role

router = APIRouter()

@router.post("/voice/stt")
async def voice_stt(
    file: UploadFile = File(...),
    fingerprint: Optional[str] = Form(None),
    role: str = Depends(get_role),
):
    if role != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="admin_only")

    content = await file.read()
    size_kb = round(len(content) / 1024, 2)
    return {
        "status": "ok",
        "engine": "placeholder",
        "fingerprint": fingerprint,
        "size_kb": size_kb,
        "text": f"تم استلام ملف صوتي ({size_kb} KB). يمكن ربط STT حقيقي لاحقاً."
    }
