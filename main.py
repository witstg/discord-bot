import time
import requests
import re
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from discord_webhook import DiscordWebhook

# Lista stron do monitorowania
URLS = [
    "https://example.com/page1",  # Zamień na swoje strony
    "https://example.com/page2",
    # Dodaj więcej URLi
]

# Discord webhook URL
DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/your-webhook-id"

# Wzorzec do wyszukiwania adresów IP
IP_PATTERN = r'\b(?:\d{1,3}\.){3}\d{1,3}\b'

def create_driver():
    options = Options()
    options.add_argument("--headless")  # Używaj przeglądarki bez GUI
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    service = Service("path_to_chromedriver")  # Zaktualizuj ścieżkę do chromedriver
    driver = webdriver.Chrome(service=service, options=options)
    return driver

def check_pages(driver):
    for url in URLS:
        try:
            driver.get(url)
            time.sleep(3)  # Poczekaj, aż strona się załaduje

            # Pobierz HTML i szukaj IP
            html = driver.page_source
            ips = re.findall(IP_PATTERN, html)
            if len(ips) >= 2:
                message = f"🔍 Na stronie {url} znaleziono 2 lub więcej adresów IP:\n{', '.join(ips)}"
                send_discord_notification(message)
        except Exception as e:
            print(f"❌ Błąd podczas sprawdzania {url}: {e}")

def send_discord_notification(message):
    webhook = DiscordWebhook(url=DISCORD_WEBHOOK_URL, content=message)
    response = webhook.execute()
    if response.status_code == 200:
        print(f"✅ Powiadomienie wysłane: {message}")
    else:
        print(f"❌ Błąd wysyłania powiadomienia: {response.status_code}")

def main():
    driver = create_driver()
    while True:
        check_pages(driver)
        time.sleep(60)  # Sprawdzaj strony co minutę

if __name__ == "__main__":
    main()
