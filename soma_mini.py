import requests
from sentence_transformers import SentenceTransformer
import numpy as np
import json

class SomaFree:
    """
    %100 Ücretsiz SOMA - Ollama kullanıyor
    """
    def __init__(self, ollama_url="http://localhost:11434"):
        print("🧠 SOMA (Ücretsiz Versiyon) başlatılıyor...")
        
        # Embedding modeli (ücretsiz, yerelde çalışır)
        print("📥 Embedding modeli yükleniyor...")
        self.embedding_model = SentenceTransformer(
            'emrecan/bert-base-turkish-cased-mean-nli-stsb-tr'
        )
        
        # Ollama bağlantısı
        self.ollama_url = ollama_url
        self.model_name = "llama3.1:8b"  # Kullanılacak model
        
        # Ollama'nın çalışıp çalışmadığını kontrol et
        self._check_ollama()
        
        print("✅ SOMA hazır!")
    
    def _check_ollama(self):
        """Ollama'nın çalışıp çalışmadığını kontrol et"""
        try:
            response = requests.get(f"{self.ollama_url}/api/tags")
            if response.status_code == 200:
                models = response.json().get('models', [])
                model_names = [m['name'] for m in models]
                
                if self.model_name not in model_names:
                    print(f"⚠️  {self.model_name} modeli bulunamadı!")
                    print(f"   Terminalde şunu çalıştır: ollama pull {self.model_name}")
                    raise Exception(f"Model yok: {self.model_name}")
                else:
                    print(f"✅ Ollama bağlantısı başarılı ({self.model_name})")
        except requests.exceptions.ConnectionError:
            print("❌ Ollama'ya bağlanılamıyor!")
            print("   Terminalde şunu çalıştır: ollama serve")
            raise
    
    def anlamsal_arama(self, sorgu, kayitlar, top_k=3):
        """
        Anlamsal arama yapan ana fonksiyon
        """
        print(f"\n🔍 Aranan: '{sorgu}'")
        
        # 1. Sorguyu vektöre çevir
        sorgu_vektoru = self.embedding_model.encode(sorgu)
        
        # 2. Tüm kayıtları vektöre çevir
        kayit_metinleri = [k["notlar"] for k in kayitlar]
        kayit_vektorleri = self.embedding_model.encode(kayit_metinleri)
        
        # 3. Benzerlik hesapla (cosine similarity)
        benzerlikler = []
        for i, kayit_vektoru in enumerate(kayit_vektorleri):
            benzerlik = np.dot(sorgu_vektoru, kayit_vektoru) / (
                np.linalg.norm(sorgu_vektoru) * np.linalg.norm(kayit_vektoru)
            )
            benzerlikler.append({
                "kayit": kayitlar[i],
                "skor": float(benzerlik)
            })
        
        # 4. Skora göre sırala
        benzerlikler.sort(key=lambda x: x["skor"], reverse=True)
        
        print(f"\n📊 En yakın {top_k} sonuç:")
        for i, sonuc in enumerate(benzerlikler[:top_k], 1):
            print(f"{i}. {sonuc['kayit']['isim']} (Skor: {sonuc['skor']:.3f})")
            print(f"   Not: {sonuc['kayit']['notlar'][:60]}...")
        
        return benzerlikler[:top_k]
    
    def llm_ile_cevapla(self, sorgu, bulunan_kayitlar):
        """
        Ollama ile doğal dil yanıtı üret
        """
        # Kayıtları prompt için hazırla
        kayit_metni = "\n\n".join([
            f"Hasta {i+1}: {k['kayit']['isim']}\n"
            f"Tarih: {k['kayit']['tarih']}\n"
            f"Notlar: {k['kayit']['notlar']}\n"
            f"Benzerlik Skoru: {k['skor']:.2f}"
            for i, k in enumerate(bulunan_kayitlar)
        ])
        
        prompt = f"""Sen bir terapist asistanısın. Hasta kayıtlarında arama yaptın ve sonuçları kullanıcıya açıklaman gerekiyor.

KULLANICI SORUSU: {sorgu}

BULUNAN KAYITLAR:
{kayit_metni}

Lütfen kullanıcıya, bulduğun en alakalı hasta/hastaları kısa ve öz bir şekilde açıkla. Hasta gizliliğine dikkat et ama yardımcı ol. Türkçe yanıt ver."""

        print("\n🤖 Ollama cevap hazırlıyor...")
        
        try:
            # Ollama API'sine istek gönder
            response = requests.post(
                f"{self.ollama_url}/api/generate",
                json={
                    "model": self.model_name,
                    "prompt": prompt,
                    "stream": False,
                    "options": {
                        "temperature": 0.7,
                        "num_predict": 256  # Maksimum token sayısı
                    }
                },
                timeout=60  # 60 saniye timeout
            )
            
            if response.status_code == 200:
                result = response.json()
                return result['response'].strip()
            else:
                return f"❌ Ollama hatası: {response.status_code}"
                
        except requests.exceptions.Timeout:
            return "⏱️ Zaman aşımı - Ollama yanıt vermedi (60 saniye)"
        except Exception as e:
            return f"❌ Hata: {str(e)}"
    
    def llm_ile_cevapla_streaming(self, sorgu, bulunan_kayitlar):
        """
        Stream modunda cevap (kelime kelime yazıyor gibi)
        """
        kayit_metni = "\n\n".join([
            f"Hasta {i+1}: {k['kayit']['isim']}\n"
            f"Tarih: {k['kayit']['tarih']}\n"
            f"Notlar: {k['kayit']['notlar']}\n"
            f"Benzerlik Skoru: {k['skor']:.2f}"
            for i, k in enumerate(bulunan_kayitlar)
        ])
        
        prompt = f"""Sen bir terapist asistanısın. Hasta kayıtlarında arama yaptın.

KULLANICI SORUSU: {sorgu}

BULUNAN KAYITLAR:
{kayit_metni}

Kısa ve öz açıkla. Türkçe yanıt ver."""

        print("\n🤖 Ollama cevap hazırlıyor (stream)...")
        
        try:
            response = requests.post(
                f"{self.ollama_url}/api/generate",
                json={
                    "model": self.model_name,
                    "prompt": prompt,
                    "stream": True,
                    "options": {"temperature": 0.7}
                },
                stream=True,
                timeout=60
            )
            
            full_response = ""
            for line in response.iter_lines():
                if line:
                    chunk = json.loads(line)
                    if 'response' in chunk:
                        token = chunk['response']
                        print(token, end='', flush=True)
                        full_response += token
            
            print()  # Yeni satır
            return full_response.strip()
            
        except Exception as e:
            return f"❌ Hata: {str(e)}"