# AI Art Starter (5 categorieën)

Dit project maakt automatisch AI-plaatjes in 5 categorieën en zet ze klaar voor sociale media en Etsy.

## Pipeline
1. `python generate.py`  
   → genereert 2–3 beelden per categorie via Stable Diffusion (Automatic1111 API, bv. RunPod).  
   Uitvoer: `niches/<categorie>/out/raw/`

2. `python postprocess.py`  
   → voegt watermark toe en maakt varianten (1:1, 9:16, 16:9).  
   Uitvoer: `out/final/` en `out/variants/`

3. `python catalog.py`  
   → maakt `schedule.csv` met geplande posts (caption + hashtags).  
   Dit CSV-bestand kun je uploaden in **Buffer** of **Metricool** voor automatische social posts.

## Setup
- Installeer **Python 3.10+** op je laptop.
- Installeer de vereisten:
  pip install -r requirements.txt
- Kopieer `.env.example` → `.env` en vul in:
  - `A1111_URL` = jouw Stable Diffusion server (bijv. RunPod URL)  
  - `TIMEZONE` = Europe/Amsterdam  
  - `IMAGES_PER_NICHE` = aantal plaatjes per categorie per dag
- Plaats een transparante PNG-watermark in `shared/logo.png` (mag leeg of tijdelijk nepbestand zijn).

## Draaien
Voer deze commando’s uit in de projectmap:
  python generate.py
  python postprocess.py
  python catalog.py

Na afloop:
- Nieuwe plaatjes staan in `niches/.../out/`
- `schedule.csv` staat in de hoofdmap → upload dit in Buffer/Metricool om automatisch te posten.
