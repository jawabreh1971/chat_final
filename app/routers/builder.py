from fastapi import APIRouter, Body, Depends, HTTPException, status
from app.auth import get_role

router = APIRouter()
BUILDER_DB = {}  # محاكاة مكان حفظ المشاريع

@router.post("/builder/create")
async def builder_create(fingerprint: str = Body(...), project_name: str = Body(...), project_type: str = Body(...), spec: str = Body(...), role: str = Depends(get_role)):
    if role != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="admin_only")
    
    BUILDER_DB[project_name] = {"type": project_type, "spec": spec, "fingerprint": fingerprint}
    return {"status": "ok", "download_url": f"/builder/download/{project_name}.zip"}

@router.get("/builder/download/{project_name}")
async def builder_download(project_name: str, role: str = Depends(get_role)):
    if role != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="admin_only")
    
    if project_name not in BUILDER_DB:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="project_not_found")
    
    return {"status": "ok", "message": f"حزمة المشروع {project_name} جاهزة للتحميل (placeholder)."}
