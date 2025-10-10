from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from soma_mini import SomaFree
from demo_data import HASTA_KAYITLARI
import json

app = FastAPI(
    title="SOMA Demo API (Ücretsiz)",
    description="Ollama tabanlı anlamsal arama API'si"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# SOMA'yı başlat
try:
    soma = SomaFree()
    print("✅ API hazır!")
except Exception as e:
    print(f"❌ SOMA başlatılamadı: {e}")
    soma = None

class SorguRequest(BaseModel):
    sorgu: str
    top_k: int = 3
    stream: bool = False

@app.get("/")
def anasayfa():
    if soma is None:
        raise HTTPException(status_code=503, detail="SOMA başlatılamadı")
    return {
        "mesaj": "SOMA API (Ücretsiz) çalışıyor! ✅",
        "model": "Ollama + Llama 3.1:8b",
        "maliyet": "₺0"
    }

@app.get("/health")
def health_check():
    """Sistem durumu kontrolü"""
    if soma is None:
        return {"status": "error", "message": "SOMA başlatılamadı"}
    
    try:
        # Ollama'nın çalışıp çalışmadığını kontrol et
        import requests
        response = requests.get("http://localhost:11434/api/tags", timeout=2)
        ollama_ok = response.status_code == 200
    except:
        ollama_ok = False
    
    return {
        "status": "healthy" if ollama_ok else "degraded",
        "soma": "ready",
        "ollama": "connected" if ollama_ok else "disconnected"
    }

@app.post("/ara")
def ara(request: SorguRequest):
    """Anlamsal arama endpoint'i"""
    if soma is None:
        raise HTTPException(status_code=503, detail="SOMA hazır değil")
    
    try:
        sonuclar = soma.anlamsal_arama(
            request.sorgu, 
            HASTA_KAYITLARI, 
            request.top_k
        )
        
        yanit = soma.llm_ile_cevapla(request.sorgu, sonuclar)
        
        return {
            "sorgu": request.sorgu,
            "sonuclar": sonuclar,
            "llm_yanit": yanit,
            "model": "llama3.1:8b",
            "maliyet": "₺0"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/kayitlar")
def tum_kayitlar():
    """Tüm hasta kayıtlarını döndür"""
    return {"kayitlar": HASTA_KAYITLARI, "toplam": len(HASTA_KAYITLARI)}

@app.get("/models")
def available_models():
    """Kullanılabilir Ollama modelleri"""
    try:
        import requests
        response = requests.get("http://localhost:11434/api/tags")
        if response.status_code == 200:
            return response.json()
        return {"error": "Ollama'ya ulaşılamıyor"}
    except:
        return {"error": "Ollama çalışmıyor"}
    