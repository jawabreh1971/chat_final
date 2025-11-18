from fastapi import APIRouter, Depends, HTTPException, status
from fastapi import Body, Query
from typing import Dict, Any, List, Optional
from app.auth import get_role

router = APIRouter()
MEMORY_DB = {}  # محاكاة قاعدة بيانات بسيطة

@router.post("/memory/save")
async def save_memory(fingerprint: str = Body(...), key: str = Body(...), value: Any = Body(...), role: str = Depends(get_role)):
    if role != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="admin_only")
    
    if fingerprint not in MEMORY_DB:
        MEMORY_DB[fingerprint] = []
    
    MEMORY_DB[fingerprint].append({"id": len(MEMORY_DB[fingerprint])+1, "key": key, "value": value})
    return {"status": "ok", "message": "تم حفظ الذاكرة بنجاح."}

@router.get("/memory/list")
async def list_memory(fingerprint: str = Query(...), role: str = Depends(get_role)):
    if role != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="admin_only")
    
    items = MEMORY_DB.get(fingerprint, [])
    return {"status": "ok", "items": items}
