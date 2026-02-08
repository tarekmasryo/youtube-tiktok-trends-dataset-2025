# 🎬 YouTube Shorts & TikTok Trends 2025 (Synthetic)

A **synthetic, analysis-ready** snapshot of short-form video performance on **TikTok** and **YouTube Shorts** (2025-01-01 → 2025-08-31).

- **Raw table:** 48,079 videos × 58 columns  
- **ML-ready table:** 50,000 rows × 32 columns  
- **Coverage:** 30 ISO-2 countries · 2 platforms  
- **Labels:** `rising` · `stable` · `declining` · `seasonal`  
- **Safe by design:** creator handles, titles, and comments are **synthetic** (no real user records)

---

## 📦 Files

| File | Rows × Cols | What it’s for |
|---|---:|---|
| `data/youtube_shorts_tiktok_trends_2025.csv` | 48,079 × 58 | video-level analytics (engagement, metadata, text fields) |
| `data/youtube_shorts_tiktok_trends_2025_ml.csv` | 50,000 × 32 | simplified, feature-engineered table for baselines |
| `data/monthly_trends_2025.csv` | 480 × 8 | monthly rollups (country × platform × month) |
| `data/country_platform_summary_2025.csv` | 60 × 14 | benchmarks by country × platform |
| `data/top_hashtags_2025.csv` | 82 × 18 | hashtag-level rollups |
| `data/top_creators_impact_2025.csv` | 1,000 × 20 | creator-level rollups |
| `data/DATA_DICTIONARY.csv` | 58 × 2 | column descriptions for the raw file |
| `docs/DATA_DICTIONARY.md` | — | readable data dictionary (raw + ML-ready) |

---

## 🧾 Quickstart

```python
import pandas as pd

raw = pd.read_csv("data/youtube_shorts_tiktok_trends_2025.csv")
ml  = pd.read_csv("data/youtube_shorts_tiktok_trends_2025_ml.csv")

print(raw.shape, ml.shape)
print(raw[["platform", "country", "views", "likes", "comments", "shares"]].head())
```

---

## ✅ Data quality (reproducible)

Install minimal deps:

```bash
pip install -r requirements.txt -r requirements-dev.txt
```

Run validations:

```bash
python scripts/validate_dataset.py
python scripts/make_checksums.py --check
```

Notes:
- Checksums are generated for **data files** under `data/` (not for scripts/requirements).
- Country codes are normalized to **uppercase ISO‑2**.

---

## 📜 License

Released under **CC BY 4.0**. See `LICENSE`.

---

## 🧷 Citation

If you use this dataset, please cite **`CITATION.cff`**.
