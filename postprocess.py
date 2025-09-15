from pathlib import Path
from PIL import Image

WM_PATH = Path("shared/logo.png")

def save_ratio(im, target_ratio, outpath):
    W, H = im.size
    if W / H > target_ratio:
        newW = int(H * target_ratio); x = (W - newW) // 2; box = (x, 0, x + newW, H)
    else:
        newH = int(W / target_ratio); y = (H - newH) // 2; box = (0, y, W, y + newH)
    im2 = im.crop(box)
    new_w = 1080
    new_h = int(new_w / target_ratio)
    im2 = im2.resize((new_w, new_h))
    im2.convert("RGB").save(outpath, quality=90, optimize=True)

def main():
    if not WM_PATH.exists():
        print("[WARN] Geen shared/logo.png gevonden — ga door zonder watermark.")
    else:
        WM = Image.open(WM_PATH).convert("RGBA")

    for niche in [p for p in Path("niches").iterdir() if p.is_dir()]:
        raw = niche/"out"/"raw"; final = niche/"out"/"final"; variants = niche/"out"/"variants"
        final.mkdir(parents=True, exist_ok=True); variants.mkdir(parents=True, exist_ok=True)
        for f in raw.glob("*.png"):
            im = Image.open(f).convert("RGBA")
            # watermark 12% breed rechtsonder (indien aanwezig)
            if WM_PATH.exists():
                w = max(64, int(im.width*0.12))
                wm = WM.resize((w, int(WM.height*w/WM.width)))
                composed = im.copy()
                composed.alpha_composite(wm, (im.width - wm.width - 30, im.height - wm.height - 30))
            else:
                composed = im
            out_final = (final/f.name).with_suffix(".jpg")
            composed.convert("RGB").save(out_final, quality=92, optimize=True)

            # Variants
            save_ratio(composed, 1.0, variants/(f.stem + "_1x1.jpg"))
            save_ratio(composed, 9/16, variants/(f.stem + "_9x16.jpg"))
            save_ratio(composed, 16/9, variants/(f.stem + "_16x9.jpg"))

            print("processed:", f)

if __name__ == "__main__":
    main()
