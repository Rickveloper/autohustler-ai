import json
import os
import requests
from PIL import Image
from io import BytesIO

OUTPUT_DIR = "../products"
API_URLS = [
    "http://localhost:8188/generate",     # ComfyUI API extension
    "http://127.0.0.1:5000/generate",     # AUTOMATIC1111 / SD-WebUI API
]

PROMPT_TEMPLATE = "A clean, minimalistic 4k book cover for a nonfiction ebook titled: '{}'. Neutral background, centered title, sharp lighting, elegant vibe."

def auto_detect_sd_api():
    for url in API_URLS:
        try:
            r = requests.get(url.replace("/generate", "/"))
            if r.status_code in [200, 404]:  # OK or endpoint not found (but server is up)
                return url
        except requests.exceptions.ConnectionError:
            continue
    return None

def generate_cover(title, save_path):
    prompt = PROMPT_TEMPLATE.format(title)
    print(f"Generating cover for: {title}")
    
    api_url = auto_detect_sd_api()
    if not api_url:
        print("❌ No local SD API detected. Saving prompt to prompt.txt instead.")
        with open(os.path.join(save_path, "prompt.txt"), "w") as f:
            f.write(prompt)
        return
    
    payload = {
        "prompt": prompt,
        "width": 1600,
        "height": 2560,
        "steps": 30,
        "cfg_scale": 7.5,
        "sampler": "Euler a"
    }

    try:
        res = requests.post(api_url, json=payload)
        res.raise_for_status()
        image = Image.open(BytesIO(res.content))
        image.save(os.path.join(save_path, "cover.png"))
        print("✅ Cover saved")
    except Exception as e:
        print(f"🚨 Error generating cover: {e}")

def find_latest_product_dir():
    dirs = [os.path.join(OUTPUT_DIR, d) for d in os.listdir(OUTPUT_DIR)]
    dirs = [d for d in dirs if os.path.isdir(d)]
    return max(dirs, key=os.path.getmtime)

if __name__ == "__main__":
    latest = find_latest_product_dir()
    with open(os.path.join(latest, "meta.json"), "r") as f:
        meta = json.load(f)
    generate_cover(meta.get("title", "Untitled"), latest)
