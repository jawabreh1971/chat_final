from fastapi import APIRouter, UploadFile, File, Depends, HTTPException, status

# Placeholder لدالة التحقق من الدور
def get_role():
    return "admin"

router = APIRouter()

@router.post("/vision/ocr")
async def vision_ocr(image: UploadFile = File(...), role: str = Depends(get_role)):
    if role != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="admin_only")

    content = await image.read()
    size_kb = round(len(content) / 1024, 2)
    return {
        "status": "ok",
        "engine": "placeholder",
        "size_kb": size_kb,
        "text": "تم استلام صورة بنجاح. المحرك الفعلي يمكن إضافته لاحقاً."
    }
