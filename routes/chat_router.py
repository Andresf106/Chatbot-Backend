from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import google.generativeai as genai
import os
import logging

# =========================
# Router
# =========================
router = APIRouter(
    prefix="/chat",
    tags=["Chat IA"]
)

# =========================
# Configuración Gemini
# =========================
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    logging.warning("⚠️ GEMINI_API_KEY no encontrada")
else:
    genai.configure(api_key=GEMINI_API_KEY)

# =========================
# Modelos (Schemas)
# =========================
class ChatRequest(BaseModel):
    mensaje: str

class ChatResponse(BaseModel):
    respuesta: str

# =========================
# Endpoint Chat
# =========================
@router.post("/", response_model=ChatResponse)
async def chat(req: ChatRequest):

    if not GEMINI_API_KEY:
        raise HTTPException(
            status_code=500,
            detail="Gemini no configurado"
        )

    try:
        # ✅ MODELO CORRECTO Y ESTABLE
        model = genai.GenerativeModel(
            model_name="models/gemini-1.5-flash",
            system_instruction=(
                "Eres Help Medic, un asistente médico informativo. "
                "No das diagnósticos ni recetas. "
                "Respondes de forma clara, breve y educativa."
            )
        )

        response = model.generate_content(req.mensaje)

        return ChatResponse(
            respuesta=response.text
        )

    except Exception as e:
        logging.error(f"❌ Error Gemini: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error en Gemini: {str(e)}"
        )
