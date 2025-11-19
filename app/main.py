from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware

from app.routers import files, vision, builder, chat, memory, voice  # استدعاء الروترات
import os
import openai
from app.autopilot_v7 import autopilot_router

# التحقق من وجود مفتاح OpenAI في البيئة
openai.api_key = os.environ.get("OPENAI_API_KEY")
if not openai.api_key:
    raise RuntimeError("OPENAI_API_KEY is not set in environment variables")

app = FastAPI(title="PAI6 Backend")

# إعداد CORS
origins = [
    "http://localhost:8000",
    "http://127.0.0.1:8000",
    "https://pai6-frontend.onrender.com", 
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# تضمين الروترات
app.include_router(files.router, prefix="/api")
app.include_router(vision.router, prefix="/api")
app.include_router(builder.router, prefix="/api")
app.include_router(chat.router, prefix="/api")
app.include_router(memory.router, prefix="/api")
app.include_router(voice.router, prefix="/api")
app.include_router(autopilot_router, prefix="/api")
# ملفات ثابتة
app.mount("/static", StaticFiles(directory=os.path.join(os.path.dirname(__file__), "static")), name="static")

# Templates
templates = Jinja2Templates(directory=os.path.join(os.path.dirname(__file__), "templates"))

# صفحة رئيسية تعرض index.html
@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/healthz")
def health_check():
    return {"status": "ok"}
