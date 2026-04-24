import os
import requests

IMAGES_DIR = "images"

# پوشه خروجی را بساز اگر وجود ندارد
if not os.path.exists(IMAGES_DIR):
    os.makedirs(IMAGES_DIR)

# خواندن لینک‌ها از فایل links.txt
with open("links.txt", "r") as f:
    links = [line.strip() for line in f.readlines() if line.strip()]

for url in links:
    try:
        filename = url.split("/")[-1]
        output_path = os.path.join(IMAGES_DIR, filename)

        print(f"Downloading: {url}")
        response = requests.get(url, timeout=30)

        # ذخیره فایل
        with open(output_path, "wb") as img:
            img.write(response.content)

        print(f"Saved: {output_path}")

    except Exception as e:
        print(f"Failed to download {url}: {e}")
