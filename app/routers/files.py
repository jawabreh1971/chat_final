import os
from fastapi import APIRouter, UploadFile, File, Form, Depends, HTTPException, status
from typing import List, Optional

# Placeholder لدالة التحقق من الدور
def get_role():
    return "admin"

router = APIRouter()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
UPLOADS_ROOT = os.path.join(BASE_DIR, "uploads")
os.makedirs(UPLOADS_ROOT, exist_ok=True)

@router.post("/files/upload")
async def files_upload(
    files: List[UploadFile] = File(...),
    fingerprint: Optional[str] = Form(None),
    category: Optional[str] = Form(None),
    role: str = Depends(get_role),
):
    if role != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="admin_only")

    saved_files = []
    for uf in files:
        filename = uf.filename or "unnamed"
        target_path = os.path.join(UPLOADS_ROOT, filename)
        content = await uf.read()
        with open(target_path, "wb") as f:
            f.write(content)
        saved_files.append({"name": filename, "size": len(content)})

    return {
        "status": "ok",
        "fingerprint": fingerprint,
        "category": category,
        "files_count": len(saved_files),
        "files": saved_files,
        "note": "تم حفظ الملفات فقط. التحليل الحقيقي يمكن إضافته لاحقاً."
    }
