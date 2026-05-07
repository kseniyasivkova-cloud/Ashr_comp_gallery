import os
import re
import time
import json
import requests
import warnings
warnings.filterwarnings("ignore")

APP_IDS = [
    # Контентные wellness-платформы
    "571800810",    # Calm
    "493145008",    # Headspace
    "337472899",    # Insight Timer
    "1361356590",   # Balance
    "1114223104",   # Aura
    "1426525843",   # BetterSleep
    "1077776989",   # Tide
    # Функциональный аудио-wellness
    "1827349267",   # Endel
    "1110684238",   # Brain.fm
    "862773459",    # Noisli
    "478687481",    # Rain Rain Sleep Sounds
    # Anti-scroll / attention control
    "1497465230",   # Opal
    "1532875441",   # one sec
    "1269788228",   # Freedom
    "866450515",    # Forest
    "1658592224",   # Stay Focused
    # Experience-first / immersive
    "1465238901",   # Loóna
    "1436994560",   # Portal
    "1465149118",   # TRIPP
    "1461517107",   # Mesmerize
]

ROOT_DIR = "app_screenshots"

def sanitize_name(name):
    name = re.sub(r'[\\/*?:"<>|]', '', name)
    name = name.strip().replace('  ', ' ')
    return name[:80]

def extract_id(raw):
    raw = raw.strip()
    m = re.search(r'id(\d+)', raw)
    if m:
        return m.group(1)
    if raw.isdigit():
        return raw
    return raw

def download_image(url, path, session):
    try:
        resp = session.get(url, timeout=30)
        resp.raise_for_status()
        with open(path, 'wb') as f:
            f.write(resp.content)
        return True
    except Exception as e:
        print(f"    ⚠ Ошибка скачивания {url}: {e}")
        return False

def fetch_app(app_id, session):
    url = f"https://itunes.apple.com/lookup?id={app_id}&country=us"
    try:
        resp = session.get(url, timeout=15)
        resp.raise_for_status()
        data = resp.json()
        if data.get("resultCount", 0) == 0:
            print(f"  ✗ Приложение {app_id} не найдено в API")
            return None
        return data["results"][0]
    except Exception as e:
        print(f"  ✗ Ошибка API для {app_id}: {e}")
        return None

def main():
    os.makedirs(ROOT_DIR, exist_ok=True)
    session = requests.Session()
    session.headers.update({"User-Agent": "Mozilla/5.0"})

    total_apps = 0
    total_screenshots = 0
    results = []

    for raw_id in APP_IDS:
        app_id = extract_id(raw_id)
        print(f"\n→ Обрабатываю ID: {app_id}")

        info = fetch_app(app_id, session)
        time.sleep(1.5)

        if not info:
            continue

        name = info.get("trackName", f"app_{app_id}")
        safe_name = sanitize_name(name)
        app_dir = os.path.join(ROOT_DIR, safe_name)
        os.makedirs(app_dir, exist_ok=True)

        iphone_urls = info.get("screenshotUrls", [])
        ipad_urls   = info.get("ipadScreenshotUrls", [])

        print(f"  ✓ {name}: {len(iphone_urls)} iPhone, {len(ipad_urls)} iPad скриншотов")

        app_count = 0

        for i, url in enumerate(iphone_urls, start=1):
            # Запрашиваем полное разрешение (замена размерной части URL)
            full_url = re.sub(r'\d+x\d+bb', '1080x1920bb', url)
            path = os.path.join(app_dir, f"iphone_{i:02d}.jpg")
            if download_image(full_url, path, session):
                app_count += 1
            time.sleep(0.3)

        for i, url in enumerate(ipad_urls, start=1):
            full_url = re.sub(r'\d+x\d+bb', '2048x2732bb', url)
            path = os.path.join(app_dir, f"ipad_{i:02d}.jpg")
            if download_image(full_url, path, session):
                app_count += 1
            time.sleep(0.3)

        total_apps += 1
        total_screenshots += app_count
        results.append({
            "id": app_id,
            "name": name,
            "safe_name": safe_name,
            "folder": app_dir,
            "iphone_count": len(iphone_urls),
            "ipad_count": len(ipad_urls),
            "downloaded": app_count,
        })

    # Сохраняем метаданные для генерации галереи
    with open(os.path.join(ROOT_DIR, "metadata.json"), "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    print(f"\n{'='*50}")
    print(f"Готово! Обработано приложений: {total_apps}")
    print(f"Всего скачано скриншотов:      {total_screenshots}")
    return results

if __name__ == "__main__":
    main()
