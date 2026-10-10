import datetime
import os
import threading
import time
from http.server import BaseHTTPRequestHandler, HTTPServer
import requests
import schedule


# 1. Render'ın port tarama (port scan) kuralını karşılayan hafif web sunucusu
class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Form Otomasyonu Bulutta Aktif!")


def run_web_server():
    port = int(os.environ.get("PORT", 10000))
    server = HTTPServer(("0.0.0.0", port), SimpleHTTPRequestHandler)
    server.serve_forever()


# 2. Form Gönderim Fonksiyonu
def form_gonder():
    bugun = datetime.datetime.now().weekday()
    if bugun == 6:  # Pazar günü çalışmasın
        print("Bugün Pazar, form gönderilmedi.", flush=True)
        return

    url = "https://docs.google.com/forms/d/e/1FAIpQLSeYuI6376usUPIpt5Ff_jymp142bzZ588cJyhw3x9PD2v60Fw/formResponse"

    payload = {
        "entry.731658915": "Mehmet Türlüdür",
        "entry.1441346099": "Ankara İade",
        "entry.1534287904": "1 Numaralı Picker",
        "entry.750096179": "Uygun",
        "entry.2015368287": "Uygun",
        "entry.2017718751": "Uygun",
        "entry.1730362896": "Uygun",
        "entry.1867001235": "Uygun",
        "entry.1148743416": "Uygun",
        "entry.1136053129": "Uygun",
    }

    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        )
    }

    try:
        res = requests.post(url, data=payload, headers=headers)
        print(f"Form gönderildi! Yanıt Kodu: {res.status_code}", flush=True)
    except Exception as e:
        print(f"Hata oluştu: {e}", flush=True)


# Web sunucusunu arka planda başlat (Render port hatasını engeller)
server_thread = threading.Thread(target=run_web_server, daemon=True)
server_thread.start()

# Zamanlayıcılar (TR Saati UTC+3 -> 07:00 için 04:00 UTC, 23:00 için 20:00 UTC)
schedule.every().day.at("04:00").do(form_gonder)
schedule.every().day.at("20:00").do(form_gonder)

print(
    "Otomasyon bulutta başlatıldı. Tetiklenme bekleniyor...",
    flush=True,
)

while True:
    schedule.run_pending()
    time.sleep(60)
