import os
import requests
import time
from urllib.parse import urlparse

IMAGES_DIR = "images"
FAILED_FILE = "failed.txt"
RETRY_COUNT = 3
RETRY_DELAY = 2

def get_filename_from_url(url):
    # استخراج نام فایل از آخرین بخش URL
    parsed = urlparse(url)
    path = parsed.path
    filename = os.path.basename(path)
    if not filename or len(filename) < 5:
        filename = "unknown.jpg"
    # اطمینان از اینکه پسوند دارد
    if not any(filename.lower().endswith(ext) for ext in ['.jpg','.jpeg','.png','.gif','.webp']):
        filename += ".jpg"
    return filename

def download_image(url, output_path, headers):
    for attempt in range(RETRY_COUNT):
        try:
            response = requests.get(url, headers=headers, timeout=30)
            if response.status_code == 200:
                # بررسی اینکه محتوا تصویر است
                content_type = response.headers.get('content-type', '')
                if 'image' in content_type:
                    with open(output_path, "wb") as f:
                        f.write(response.content)
                    return True
                else:
                    print(f"Not an image ({content_type}): {url}")
                    return False
            else:
                print(f"Attempt {attempt+1}: status {response.status_code} for {url}")
        except Exception as e:
            print(f"Attempt {attempt+1} error: {e}")
        time.sleep(RETRY_DELAY)
    return False

def main():
    # ایجاد پوشه
    if not os.path.exists(IMAGES_DIR):
        os.makedirs(IMAGES_DIR)
    
    # حذف فایل failed قبلی
    if os.path.exists(FAILED_FILE):
        os.remove(FAILED_FILE)
    
    # خواندن لینک‌ها
    if not os.path.exists("links.txt"):
        print("ERROR: links.txt not found!")
        return
    
    with open("links.txt", "r") as f:
        links = [line.strip() for line in f if line.strip()]
    
    if not links:
        print("No links found in links.txt")
        return
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "image/webp,image/apng,image/*,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9",
        "Referer": "https://www.imdb.com/",
    }
    
    failed = []
    for idx, url in enumerate(links, 1):
        print(f"[{idx}/{len(links)}] Downloading: {url[:80]}...")
        filename = get_filename_from_url(url)
        # جلوگیری از同名
        base, ext = os.path.splitext(filename)
        counter = 1
        out_path = os.path.join(IMAGES_DIR, filename)
        while os.path.exists(out_path):
            filename = f"{base}_{counter}{ext}"
            out_path = os.path.join(IMAGES_DIR, filename)
            counter += 1
        
        success = download_image(url, out_path, headers)
        if success:
            print(f"  Saved: {filename}")
        else:
            print(f"  FAILED: {url}")
            failed.append(url)
    
    if failed:
        with open(FAILED_FILE, "w", encoding="utf-8") as f:
            for url in failed:
                f.write(url + "\n")
        print(f"\nFailed: {len(failed)} links written to {FAILED_FILE}")
    else:
        print("\nAll images downloaded successfully!")

if __name__ == "__main__":
    main()
