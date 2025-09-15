import os, time, base64, random, datetime, requests
from pathlib import Path
from dotenv import load_dotenv

# Laad .env instellingen
load_dotenv()
A1111 = os.getenv("A1111_URL", "http://127.0.0.1:7860")
IMAGES_PER_NICHE = int(os.getenv("IMAGES_PER_NICHE", "2"))

# 5 categorieën
NICHES = ["castles", "cars", "women", "animals", "patterns"]

# Negatieve prompts per niche (kwaliteit/veiligheid)
NEGATIVE = {
  "castles":  "blurry, lowres, watermark, text, logo, deformed, oversaturated",
  "cars":     "blurry, lowres, watermark, text, toy-like, lowpoly, warped",
  "women":    "nsfw, underage, explicit, nudity, lowres, bad anatomy, watermark, text",
  "animals":  "blurry, lowres, watermark, text, extra limbs, distorted",
  "patterns": "lowres, noisy, watermark, text, distorted edges"
}

# Basisinstellingen voor Automatic1111 txt2img
PAYLOAD_TEMPLATE = {
  "sampler_name": "DPM++ 2M Karras",
  "steps": 24,
  "cfg_scale": 6.5,
  "width": 1024,
  "height": 1536   # 2:3 portret (9:16/1:1 maken we later in postprocess)
}

def ensure_dirs(niche):
    (Path(f"niches/{niche}/out/raw")).mkdir(parents=True, exist_ok=True)

def txt2img(prompt, negative, seed):
    payload = {**PAYLOAD_TEMPLATE, "prompt": prompt, "negative_prompt": negative, "seed": seed}
    r = requests.post(f"{A1111}/sdapi/v1/txt2img", json=payload, timeout=600)
    r.raise_for_status()
    return r.json()["images"][0]

def main():
    today = datetime.datetime.now().strftime("%Y%m%d")
    for niche in NICHES:
        ensure_dirs(niche)
        pfile = Path(f"niches/{niche}/prompts.txt")
        if not pfile.exists():
            print(f"[WARN] ontbrekende prompts: {pfile}")
            continue
        prompts = [l.strip() for l in pfile.read_text(encoding="utf-8").splitlines() if l.strip()]
        for i in range(IMAGES_PER_NICHE):
            prompt = random.choice(prompts)
            seed = int(time.time()) + i
            print(f"[{niche}] {prompt[:80]}...")
            b64 = txt2img(prompt, NEGATIVE[niche], seed)
            img_bytes = base64.b64decode(b64.split(",")[-1])
            out = Path(f"niches/{niche}/out/raw/{niche}_{today}_{seed}_2x3.png")
            out.write_bytes(img_bytes)
            print(" saved:", out)

if __name__ == "__main__":
    main()
