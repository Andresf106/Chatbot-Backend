from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os
import logging

load_dotenv()
logging.basicConfig(level=logging.INFO)

app = FastAPI(title="Proyecto SI")

# =========================
# CORS
# =========================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =========================
# Routers
# =========================
from routes.usuario_router import router as usuario_router
from routes.doctor_router import router as doctor_router
from routes.cita_router import router as cita_router
from routes.horario_router import router as horarios_router
from routes.chat_router import router as chat_router

app.include_router(usuario_router)
app.include_router(doctor_router)
app.include_router(cita_router)
app.include_router(horarios_router)
app.include_router(chat_router)


# =========================
# Startup
# =========================
@app.on_event("startup")
async def startup_event():
    if os.getenv("GEMINI_API_KEY"):
        logging.info("✅ Gemini IA configurado correctamente")
    else:
        logging.warning("⚠️ Gemini IA NO configurado")
