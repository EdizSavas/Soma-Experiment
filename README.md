# 🧠 SOMA - Semantic Reasoning Engine

**Anlamsal Çıkarım Yapabilen Yapay Zeka Motoru**

SOMA, vektör-tabanlı anlamsal temsil ile graf-tabanlı bilgi modellemesini birleştiren hibrit bir yapay zeka mimarisidir. Klasik keyword matching'in ötesine geçerek, metinlerin içerdiği **gerçek anlam** üzerinden çıkarımlar yapar.

![SOMA Demo](https://img.shields.io/badge/version-1.0.0-purple)
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

Mimari:

┌─────────────────────────────────────────┐
│         Web Arayüzü (HTML/JS)           │
└─────────────────┬───────────────────────┘
                  │
         ┌────────▼────────┐
         │   FastAPI       │
         │   (Backend)     │
         └────────┬────────┘
                  │
    ┌─────────────┼─────────────┐
    │             │             │
┌───▼────┐  ┌────▼─────┐  ┌───▼─────┐
│ SOMA   │  │ Sentence │  │ Ollama  │
│ Motor  │  │ BERT     │  │ Llama   │
│        │  │ (Embed)  │  │ 3.2     │
└───┬────┘  └──────────┘  └─────────┘
    │
┌───▼──────────────┐
│  Vektör Arama    │
│  (Neo4j/FAISS)   │
└──────────────────┘
