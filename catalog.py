import csv, random, datetime
from pathlib import Path

HASHTAGS = {
  "castles": ["#fantasy","#castle","#aiart","#digitalart","#artdaily"],
  "cars":    ["#cars","#supercar","#conceptcar","#aiart","#cardesign"],
  "women":   ["#portrait","#editorial","#aiart","#aesthetic","#photography"],
  "animals": ["#wildlife","#animals","#nature","#aiart","#photography"],
  "patterns":["#pattern","#abstract","#design","#aiart","#texture"]
}

def main():
    start = datetime.datetime.now().replace(minute=0, second=0, microsecond=0) + datetime.timedelta(hours=1)
    with open("schedule.csv", "w", newline="", encoding="utf-8") as f:
        wr = csv.writer(f)
        wr.writerow(["datetime","platform","account","image_path","caption"])
        for niche in [p.name for p in Path("niches").iterdir() if p.is_dir()]:
            var_dir = Path(f"niches/{niche}/out/variants")
            if not var_dir.exists(): 
                continue
            for img in sorted(var_dir.glob("*_9x16.jpg")):
                dt = start
                start += datetime.timedelta(minutes=120)  # 2 uur tussen posts
                title = img.stem.replace("_", " ")
                tags = ' '.join(random.sample(HASHTAGS.get(niche, ["#aiart"]), k=min(4, len(HASHTAGS.get(niche, [])))))
                caption = f"{niche.capitalize()} — {title}\nMeer: link in bio\n{tags}"
                wr.writerow([dt.isoformat(), "instagram", niche, str(img), caption])
                print("added:", img)

if __name__ == "__main__":
    main()
