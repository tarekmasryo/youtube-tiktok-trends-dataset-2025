# 🎬 YouTube Shorts & TikTok Trends 2025  
**Author:** [Tarek Masryo](https://github.com/tarekmasryo) · [Kaggle](https://www.kaggle.com/datasets/tarekmasryo/football-matches-20242025-top-5-leagues) 

---

## 📊 TL;DR  
A **comprehensive, analysis-ready dataset** capturing YouTube Shorts & TikTok activity in **2025 (to-date)**.  

- 🌍 Coverage: 100+ countries, 2 platforms (YouTube Shorts & TikTok)  
- 📂 Multi-file package: raw video-level data, ML-ready version, monthly & country rollups, top hashtags, top creators, and a metadata dictionary  
- ⚡ Features: engagement metrics, standardized schemas, deduplicated IDs, consistent platform & country naming  

---

## 📌 Context  
Short-form video is the fastest-growing content format online.  
This dataset provides **cross-platform insights** into global short-form engagement, including:  

- Which creators drive the most engagement  
- Which hashtags dominate across platforms and regions  
- How engagement ratios (likes, comments, shares) differ between countries  
- How content categories and formats (gaming, beauty, news, etc.) perform  

💡 For machine learning tasks, please use the **ML-ready file** (`youtube_shorts_tiktok_trends_2025_ml.csv`).  
⚠️ Note: `trend_label` is a snapshot approximation (not full time-series). It’s a **challenging ML target** (≈25–35% baseline accuracy).  

Useful for **data science, dashboards, cultural research, and machine learning experiments**.  

---

## 📂 Content  

### 1. `youtube_shorts_tiktok_trends_2025.csv`  
Raw video-level data (**48,079 rows × 58 columns**).  
Includes platform, country, region, language, category, hashtags, author handles, sound/music metadata, and full engagement metrics (views, likes, comments, shares, saves).  

### 2. `youtube_shorts_tiktok_trends_2025_ml.csv`  
ML-ready version (**50,000 rows × 32 columns**).  
Simplified and feature-engineered for faster modeling and baseline machine learning tasks.  

### 3. `monthly_trends_2025.csv`  
Monthly summaries (**480 rows × 8 columns**).  
Captures video counts, views, average engagement rate, and velocity by month.  

### 4. `country_platform_summary_2025.csv`  
Aggregated statistics by country × platform (**60 rows × 14 columns**).  
Includes totals, medians, and percentile-based engagement benchmarks.  
⚠️ Note: Summary file covers 60 countries with sufficient activity; raw data spans **100+ countries**.  

### 5. `top_hashtags_2025.csv`  
Trending hashtags (**82 rows × 18 columns**).  
Tracks usage counts, reach, engagement ratios, and velocity.  

### 6. `top_creators_impact_2025.csv`  
Creator-level influence (**1,000 rows × 20 columns**).  
Includes creator handles, number of videos, cumulative views, likes, comments, shares, saves, and average engagement rates.  

### 7. `DATA_DICTIONARY.csv`  
Complete metadata (**58 rows**) with column names, descriptions, and data types.  

---

## 🌍 Coverage  
- **Time span:** January → August 2025  
- **Platforms:** YouTube Shorts, TikTok  
- **Countries:** 100+ unique markets (standardized)  
- **Records:** ~50K video-level rows + structured summaries  

---

## 📜 Licensing  
- **Dataset:** - **Dataset:** CC BY 4.0 (Attribution International)** — free to use, share, and adapt **with attribution**.


---

## Related Repositories
- 📂 [Shorts & TikTok Trends EDA](https://github.com/tarekmasryo/shorts-tiktok-trends)


---

## 💡 Example Usage  

```python
import pandas as pd

# Load ML-ready data
df = pd.read_csv("youtube_shorts_tiktok_trends_2025_ml.csv")

# Explore engagement
df[['views','likes','comments','shares']].describe()

# Track monthly growth
monthly = pd.read_csv("monthly_trends_2025.csv")
monthly.groupby("year_month")[["views","n_videos"]].sum().plot(kind="bar")




