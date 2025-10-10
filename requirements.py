import subprocess
import sys

packages = [
    "sentence-transformers",
    "fastapi",
    "uvicorn",
    "requests",
    "numpy",
    "python-dotenv"
]

def install(package):
    print(f"{package} [Yükleniyor...]")
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

def main():
    print("[+] Gerekli kütüphaneler yükleniyor...\n")
    for pkg in packages:
        try:
            install(pkg)
        except Exception as e:
            print(f"[HATA] {pkg} kurulamadı: {e}")
    print("\n[+] Yükleme tamamlandı.")

if __name__ == "__main__":
    main()
