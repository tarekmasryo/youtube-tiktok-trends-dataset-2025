# 📑 Data Dictionary — YouTube Shorts & TikTok Trends (2025)

This repo contains a **synthetic** short‑form video trends package for **TikTok** and **YouTube Shorts** (Jan → Aug 2025).

## 1) Raw video-level file

**File:** `data/youtube_shorts_tiktok_trends_2025.csv`  
**Shape:** 48,079 rows × 58 columns

| Column | Type | Description |
|--------|------|-------------|
| `platform` | `string` | Platform (TikTok/YouTube) |
| `country` | `string` | Country ISO-2 code |
| `region` | `string` | Region macro label (if available) |
| `language` | `string` | Primary language inferred from country (fallback to 'en') |
| `category` | `string` | Video category (if available) |
| `hashtag` | `string` | Primary hashtag aligned with genre |
| `title_keywords` | `string` | Short realistic title-like keywords |
| `author_handle` | `string` | Creator handle/channel (brand-like, synthetic) |
| `sound_type` | `string` | Sound type (if present) |
| `music_track` | `string` | Music track (if present) |
| `week_of_year` | `int` | ISO week number (1–53) |
| `duration_sec` | `int` | Shorts-style duration in seconds (TikTok ~5–75, YouTube ~5–90) |
| `views` | `int` | Total views |
| `likes` | `int` | Likes count |
| `comments` | `int` | Comments count |
| `shares` | `int` | Shares count |
| `saves` | `int` | Saves count |
| `engagement_rate` | `float` | (likes+comments+shares+saves) / views |
| `trend_label` | `string` | Trend snapshot label: rising / stable / declining / seasonal |
| `source_hint` | `string` | No description available |
| `notes` | `string` | No description available |
| `device_type` | `string` | Android/iOS/Web |
| `upload_hour` | `int` | Hour of day video published (0–23) |
| `genre` | `string` | Canonical content genre |
| `trend_duration_days` | `int` | Days the video remained trending (synthetic) |
| `trend_type` | `string` | Short (≤7), Medium (8–21), Evergreen (≥22) |
| `engagement_velocity` | `float` | views / trend_duration_days |
| `dislikes` | `int` | Dislikes (synthetic, platform-aware) |
| `comment_ratio` | `float` | comments / views |
| `share_rate` | `float` | shares / views |
| `save_rate` | `float` | saves / views |
| `like_dislike_ratio` | `float` | likes / (dislikes+1) |
| `publish_dayofweek` | `string` | Day of week of publish_date |
| `publish_period` | `string` | Part of day bucket (Morning/Afternoon/Evening/Night) |
| `event_season` | `string` | Seasonal/contextual event (Ramadan, SummerBreak, BackToSchool, HolidaySeason, None) |
| `tags` | `string` | YouTube-like comma-separated tags aligned with genre |
| `sample_comments` | `string` | One short synthetic multilingual comment |
| `creator_avg_views` | `float` | Avg views per video for the creator (across dataset rows) |
| `creator_tier` | `string` | Creator tier based on avg views: Micro / Mid / Macro / Star |
| `season` | `string` | Climatological season (Winter/Spring/Summer/Fall) |
| `publish_date_approx` | `string` | ISO date reconstructed/approximated within 2025 (clipped to 2025-09-12) |
| `year_month` | `string` | Publish year-month for time-series aggregation |
| `title` | `string` | Short realistic video title (synthetic) |
| `title_length` | `int` | Character count of title |
| `has_emoji` | `int` | Whether title contains emoji (1/0) |
| `avg_watch_time_sec` | `float` | Estimated average watch time (seconds) |
| `completion_rate` | `float` | avg_watch_time_sec / duration_sec |
| `device_brand` | `string` | If mobile: device brand (iPhone, Samsung, Huawei, Xiaomi, Oppo, Vivo, Pixel, Other); Web → Desktop |
| `traffic_source` | `string` | Coarse discovery source (TikTok: ForYou/Following/Search/External; YouTube: Home/Suggested/Search/External) |
| `is_weekend` | `int` | Publish on Fri/Sat/Sun = 1 |
| `row_id` | `string` | Deterministic MD5 over [platform, country, author_handle, title, publish_date_approx, duration_sec] (primary key) |
| `engagement_total` | `int` | likes + comments + shares + saves |
| `like_rate` | `float` | likes / views |
| `dislike_rate` | `float` | dislikes / views |
| `engagement_per_1k` | `float` | Total engagements per 1,000 views |
| `engagement_like_rate` | `float` | Likes divided by Views; NaN when Views <= 0 |
| `engagement_comment_rate` | `float` | Comments divided by Views; NaN when Views <= 0 |
| `engagement_share_rate` | `float` | Shares divided by Views; NaN when Views <= 0 |

---

## 2) ML-ready file

**File:** `data/youtube_shorts_tiktok_trends_2025_ml.csv`  
**Shape:** 50,000 rows × 32 columns

| Column | Type | Description |
|--------|------|-------------|
| `trend_label` | `string` | Snapshot label: `rising`, `stable`, `declining`, `seasonal` (target). |
| `platform` | `string` | Platform (`TikTok` or `YouTube`). |
| `region` | `string` | Region macro label. |
| `language` | `string` | Primary language. |
| `category` | `string` | Content category. |
| `traffic_source` | `string` | Main traffic source bucket. |
| `device_brand` | `string` | Device brand bucket. |
| `creator_tier` | `string` | Creator tier bucket. |
| `title_len` | `int` | Title length (characters). |
| `text_richness` | `float` | Simple text richness score from title/keywords. |
| `like_rate` | `float` | Likes / views. |
| `comment_rate` | `float` | Comments / views. |
| `share_rate` | `float` | Shares / views. |
| `like_rate_log` | `float` | Log-transformed like_rate. |
| `comment_rate_log` | `float` | Log-transformed comment_rate. |
| `share_rate_log` | `float` | Log-transformed share_rate. |
| `views_per_day` | `float` | Views velocity proxy. |
| `likes_per_day` | `float` | Likes velocity proxy. |
| `rel_like` | `float` | Like rate relative to platform baseline. |
| `rel_share` | `float` | Share rate relative to platform baseline. |
| `rel_combo` | `float` | Combined relative engagement signal. |
| `like_hashtag_interaction` | `float` | Interaction feature (like_rate × hashtag signal). |
| `share_hashtag_interaction` | `float` | Interaction feature (share_rate × hashtag signal). |
| `platform_cat` | `int` | Label-encoded `platform`. |
| `region_cat` | `int` | Label-encoded `region`. |
| `language_cat` | `int` | Label-encoded `language`. |
| `category_cat` | `int` | Label-encoded `category`. |
| `traffic_source_cat` | `int` | Label-encoded `traffic_source`. |
| `device_brand_cat` | `int` | Label-encoded `device_brand`. |
| `creator_tier_cat` | `int` | Label-encoded `creator_tier`. |
| `richness_traffic_interaction` | `float` | Interaction feature (text_richness × traffic_source). |
| `weekend_hashtag_boost` | `int` | Interaction feature (weekend × hashtag signal). |

---

## 3) Aggregate files

- `data/monthly_trends_2025.csv` — monthly rollups (country × platform × month)
- `data/country_platform_summary_2025.csv` — country × platform summary benchmarks
- `data/top_hashtags_2025.csv` — hashtag-level rollups
- `data/top_creators_impact_2025.csv` — creator-level rollups
