from soma_mini import SomaFree
from demo_data import HASTA_KAYITLARI

def main():
    # SOMA'yı başlat
    soma = SomaFree()
    
    print("\n" + "="*60)
    print("🎯 SOMA DEMOsu (Ücretsiz) - Kezzaplı Saldırı Arama")
    print("="*60)
    
    # Test sorgusu
    sorgu = "üzerine asit atıldığı ile ilgili sanrılar gören hasta"
    
    # 1. Anlamsal arama yap
    sonuclar = soma.anlamsal_arama(sorgu, HASTA_KAYITLARI, top_k=3)
    
    # 2. LLM ile yanıt oluştur
    print("\n" + "-"*60)
    yanit = soma.llm_ile_cevapla(sorgu, sonuclar)
    
    print("\n💬 SOMA'nın Cevabı:")
    print("-"*60)
    print(yanit)
    print("-"*60)
    
    # 3. Diğer test sorguları
    print("\n\n🔬 Başka test sorguları:")
    
    test_sorgulari = [
        "kimyasal madde korkusu olan hasta",
        "yanık tedavisi gören kimse"
    ]
    
    for sorgu in test_sorgulari:
        print(f"\n📌 Sorgu: '{sorgu}'")
        sonuclar = soma.anlamsal_arama(sorgu, HASTA_KAYITLARI, top_k=1)
        print(f"   ➜ En yakın: {sonuclar[0]['kayit']['isim']}")
    
    # 4. İnteraktif mod
    print("\n\n" + "="*60)
    print("🎮 İnteraktif Mod - 'q' yazarak çıkabilirsin")
    print("="*60)
    
    while True:
        kullanici_sorgu = input("\n🔍 Sorgunuz: ").strip()
        
        if kullanici_sorgu.lower() in ['q', 'quit', 'exit', 'çık']:
            print("👋 Görüşmek üzere!")
            break
        
        if not kullanici_sorgu:
            continue
        
        sonuclar = soma.anlamsal_arama(kullanici_sorgu, HASTA_KAYITLARI, top_k=2)
        yanit = soma.llm_ile_cevapla(kullanici_sorgu, sonuclar)
        
        print(f"\n💬 {yanit}\n")

if __name__ == "__main__":
    main()