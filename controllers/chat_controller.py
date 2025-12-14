from fastapi import APIRouter, HTTPException
from schemas.chat_schema import ChatRequest, ChatResponse
import google.generativeai as genai
import os

router = APIRouter(prefix="/chat", tags=["Chatbot"])

# API KEY
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise RuntimeError("❌ No se encontró la variable de entorno GEMINI_API_KEY")

genai.configure(api_key=GEMINI_API_KEY)

@router.post("/", response_model=ChatResponse)
async def chat_endpoint(req: ChatRequest):
    try:
        model = genai.GenerativeModel("gemini-pro")
        response = model.generate_content(req.mensaje)

        return ChatResponse(
            respuesta=response.text
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error en el chatbot: {str(e)}"
        )
