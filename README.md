# 🧠 SOMA - Semantic Reasoning Engine

**Anlamsal Çıkarım Yapabilen Yapay Zeka Motoru**

SOMA, vektör-tabanlı anlamsal temsil ile graf-tabanlı bilgi modellemesini birleştiren hibrit bir yapay zeka mimarisidir. Klasik keyword matching'in ötesine geçerek, metinlerin içerdiği **gerçek anlam** üzerinden çıkarımlar yapar.

![SOMA Demo](https://img.shields.io/badge/version-0.2.0-purple)
![Python](https://img.shields.io/badge/python-3.8+-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Status](https://img.shields.io/badge/status-pre_alpha-red)

---

## 🎯 Ne Yapar?

### Problem
Klasik arama sistemleri sadece **kelime eşleştirmesi** yapar. Örneğin:
- Kullanıcı "kezzaplı saldırı" arıyor
- Veritabanında "asit saldırısı" yazıyor
- **Klasik sistem:** Bulamaz ❌
- **SOMA:** Anlamsal olarak eşleştirir ✅

### Çözüm
SOMA, kelimelerin **anlamını** anlayarak arama yapar:
```python
Sorgu: "üzerine kezzap dökülen hasta"
        ↓ (Anlamsal Analiz)
Kavramlar: [asit, kimyasal, saldırı, yanık]
        ↓ (Vektör Benzerliği)
Sonuç: "göğsüne asit döküldüğü sanrıları gören hasta" ✅
```
---

## Hızlı Başlangıç:

### Gereksinimler

- Python 3.8+
- 8GB boş disk alanı
- 8GB RAM (önerilir)
- Ollama_3.1:8b

### Kurulum
```powershell
# 1. Repo'yu klonla
git clone https://github.com/EdizSavas/Soma-Experiment.git
cd soma-experiments

# 2. Virtual environment oluştur
python -m venv venv

# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# 3. Gereksinimleri yükle
python requirements.py
# veya
pip install -r requirements.txt

# 4. Ollama'yı başlat (yeni terminal)
ollama serve

# 5. Llama modelini indir
ollama pull llama3.1:8b
```

### Çalıştırma
```powershell
# Konsol Soma-Experiments
python demo.py

# Web API
uvicorn api:app --reload

# Web arayüzü: index_free.html dosyasını tarayıcıda aç
```

### Bilinen Sorunlar
1. İlk sorgu yavaş (model yükleme),
2. Türkçe karakter encoding bazen sorun çıkarabilir,
3. Neo4j vektör araması büyük veri setlerinde yavaş olabilir,
4. Anlam kayması ve didaktik sorunlar oluşabilir.
