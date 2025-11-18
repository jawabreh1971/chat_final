import zipfile
import os
from fastapi import APIRouter, Body, Depends, HTTPException
from fastapi.responses import FileResponse
from app.auth import get_role

router = APIRouter()

# ضمان إنشاء المجلد مهما كان مكان التشغيل
GENERATED_DIR = os.path.join(os.path.dirname(__file__), "..", "generated")
GENERATED_DIR = os.path.abspath(GENERATED_DIR)
os.makedirs(GENERATED_DIR, exist_ok=True)

@router.post("/builder/create")
async def builder_create(
    fingerprint: str = Body(...),
    project_name: str = Body(...),
    project_type: str = Body(...),
    spec: str = Body(...),
    role: str = Depends(get_role)
):
    if role != "admin":
        raise HTTPException(status_code=403, detail="admin_only")

    zip_path = os.path.join(GENERATED_DIR, f"{project_name}.zip")

    with zipfile.ZipFile(zip_path, "w") as zipf:
        zipf.writestr("info.txt", f"Project: {project_name}\nType: {project_type}\nSpec: {spec}")

    return {"status": "ok", "download_url": f"/api/builder/download/{project_name}.zip"}

@router.get("/builder/download/{filename}")
async def builder_download(filename: str, role: str = Depends(get_role)):
    if role != "admin":
        raise HTTPException(status_code=403, detail="admin_only")

    file_path = os.path.join(GENERATED_DIR, filename)

    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="file_not_found")

    return FileResponse(file_path, filename=filename, media_type="application/zip")
