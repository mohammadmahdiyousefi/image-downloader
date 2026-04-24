import os
import requests

IMAGES_DIR = "images"
FAILED_FILE = "failed.txt"

# پوشه خروجی را بساز اگر وجود ندارد
if not os.path.exists(IMAGES_DIR):
    os.makedirs(IMAGES_DIR)

# پاک کردن فایل failed.txt قدیمی اگر هست
if os.path.exists(FAILED_FILE):
    os.remove(FAILED_FILE)

# خواندن لینک‌ها از فایل links.txt
with open("links.txt", "r") as f:
    links = [line.strip() for line in f.readlines() if line.strip()]

headers = {
    # شبیه مرورگر عادی رفتار کن
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/120.0.0.0 Safari/537.36"
}

failed_links = []

for url in links:
    try:
        filename = url.split("/")[-1] or "unnamed"
        output_path = os.path.join(IMAGES_DIR, filename)

        print(f"Downloading: {url}")
        response = requests.get(url, headers=headers, timeout=30)

        if response.status_code == 200:
            with open(output_path, "wb") as img:
                img.write(response.content)
            print(f"Saved: {output_path}")
        else:
            print(f"Failed (status {response.status_code}): {url}")
            failed_links.append(f"{url} | status={response.status_code}")

    except Exception as e:
        print(f"Exception for {url}: {e}")
        failed_links.append(f"{url} | exception={e}")

# ذخیره لینک‌های مشکل‌دار در فایل
if failed_links:
    with open(FAILED_FILE, "w", encoding="utf-8") as f:
        for item in failed_links:
            f.write(item + "\n")
    print(f"\nSome downloads failed. See {FAILED_FILE} for details.")
else:
    print("\nAll images downloaded successfully.")
