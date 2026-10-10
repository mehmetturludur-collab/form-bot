import datetime
import requests
import schedule
import time


def form_gonder():
    bugun = datetime.datetime.now().weekday()
    # 6 = Pazar günü. Pazar ise çalıştırma
    if bugun == 6:
        print("Bugün Pazar, form gönderilmedi.")
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
        print(f"Form gönderildi! Yanıt Kodu: {res.status_code}")
    except Exception as e:
        print(f"Hata oluştu: {e}")


# Türkiye Saati (UTC+3) baz alınarak zamanlama:
# Render sunucuları UTC kullandığından 07:00 -> 04:00 UTC, 23:00 -> 20:00 UTC
schedule.every().day.at("04:00").do(form_gonder)
schedule.every().day.at("20:00").do(form_gonder)

print("Otomasyon bulutta başlatıldı. Tetiklenme bekleniyor...")

while True:
    schedule.run_pending()
    time.sleep(60)