"""Lightweight dataset validation (synthetic short-form trends).

This is NOT a statistical audit. It's a fast integrity + schema guardrail for:
- missing files / broken CSVs
- unexpected schema drift
- obvious range violations
- basic key constraints

Usage:
  python scripts/validate_dataset.py
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd


REPO_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = REPO_ROOT / "data"

RAW_FILE = DATA_DIR / "youtube_shorts_tiktok_trends_2025.csv"
ML_FILE = DATA_DIR / "youtube_shorts_tiktok_trends_2025_ml.csv"
MONTHLY_FILE = DATA_DIR / "monthly_trends_2025.csv"
COUNTRY_PLATFORM_FILE = DATA_DIR / "country_platform_summary_2025.csv"
TOP_HASHTAGS_FILE = DATA_DIR / "top_hashtags_2025.csv"
TOP_CREATORS_FILE = DATA_DIR / "top_creators_impact_2025.csv"
DICT_FILE = DATA_DIR / "DATA_DICTIONARY.csv"


def fail(msg: str) -> None:
    raise SystemExit(f"❌ {msg}")


def warn(msg: str) -> None:
    print(f"⚠️  {msg}")


def check_file_exists(path: Path) -> None:
    if not path.exists():
        fail(f"Missing file: {path.relative_to(REPO_ROOT)}")


def check_nonnegative(df: pd.DataFrame, cols: list[str], name: str) -> None:
    bad = []
    for c in cols:
        if c not in df.columns:
            continue
        if (df[c] < 0).any():
            bad.append(c)
    if bad:
        fail(f"{name}: negative values found in columns: {bad}")


def check_in_range(df: pd.DataFrame, col: str, lo: float, hi: float, name: str) -> None:
    if col not in df.columns:
        return
    if ((df[col] < lo) | (df[col] > hi)).any():
        sample = (
            df.loc[(df[col] < lo) | (df[col] > hi), [col]]
            .head(5)
            .to_dict(orient="records")
        )
        fail(f"{name}: {col} out of range [{lo}, {hi}]. Sample: {sample}")


def main() -> int:
    for p in [
        RAW_FILE,
        ML_FILE,
        MONTHLY_FILE,
        COUNTRY_PLATFORM_FILE,
        TOP_HASHTAGS_FILE,
        TOP_CREATORS_FILE,
        DICT_FILE,
    ]:
        check_file_exists(p)

    # Raw
    raw = pd.read_csv(RAW_FILE)
    if raw.shape[0] < 1000:
        warn(f"raw: unusually small row count: {raw.shape[0]}")

    # Required columns (schema guardrail)
    dict_df = pd.read_csv(DICT_FILE)
    expected_cols = set(dict_df["column"].astype(str).tolist())
    raw_cols = set(raw.columns.astype(str).tolist())
    missing = sorted(expected_cols - raw_cols)
    extra = sorted(raw_cols - expected_cols)
    if missing:
        fail(f"raw: missing columns vs data dictionary: {missing[:10]}")
    if extra:
        warn(f"raw: extra columns not in data dictionary: {extra[:10]}")

    # Country codes
    if "country" in raw.columns:
        bad_country = raw.loc[
            (raw["country"].astype(str).str.len() != 2)
            | (raw["country"].astype(str) != raw["country"].astype(str).str.upper()),
            ["country"],
        ].head(5)
        if not bad_country.empty:
            fail(
                f"raw: country must be uppercase ISO-2. Sample: {bad_country.to_dict(orient='records')}"
            )

    # Platform values
    if "platform" in raw.columns:
        allowed = {"TikTok", "YouTube"}
        bad = sorted(set(raw["platform"].astype(str).unique()) - allowed)
        if bad:
            fail(f"raw: unexpected platform values: {bad}")

    # Key constraint
    if "row_id" in raw.columns:
        if raw["row_id"].duplicated().any():
            fail("raw: row_id must be unique")

    # Simple ranges
    check_nonnegative(
        raw,
        cols=[
            "views",
            "likes",
            "comments",
            "shares",
            "saves",
            "dislikes",
            "creator_avg_views",
            "engagement_total",
        ],
        name="raw",
    )
    check_in_range(raw, "upload_hour", 0, 23, "raw")
    # Rates (0..1)
    for col in [
        "engagement_rate",
        "comment_ratio",
        "share_rate",
        "save_rate",
        "like_rate",
        "dislike_rate",
        "completion_rate",
        "engagement_like_rate",
        "engagement_comment_rate",
        "engagement_share_rate",
    ]:
        if col in raw.columns:
            check_in_range(raw, col, 0.0, 1.0, "raw")
    # engagement_per_1k is per-1000 metric (not a rate)
    if "engagement_per_1k" in raw.columns:
        check_in_range(raw, "engagement_per_1k", 0.0, 1000.0, "raw")

    # Dates
    if "publish_date_approx" in raw.columns and "year_month" in raw.columns:
        parsed = pd.to_datetime(raw["publish_date_approx"], errors="coerce")
        if parsed.isna().any():
            sample = (
                raw.loc[parsed.isna(), ["publish_date_approx"]]
                .head(5)
                .to_dict(orient="records")
            )
            fail(f"raw: publish_date_approx has un-parseable values. Sample: {sample}")
        ym = parsed.dt.strftime("%Y-%m")
        mismatch = (ym != raw["year_month"].astype(str)).sum()
        if mismatch > 0:
            warn(f"raw: year_month mismatches publish_date_approx in {mismatch} rows")

    # ML-ready
    ml = pd.read_csv(ML_FILE)
    required_ml = {
        "trend_label",
        "platform",
        "category",
        "like_rate",
        "comment_rate",
        "share_rate",
    }
    if not required_ml.issubset(set(ml.columns)):
        fail(f"ml: missing required columns: {sorted(required_ml - set(ml.columns))}")

    # Ensure target label values match
    allowed_labels = {"rising", "stable", "declining", "seasonal"}
    if "trend_label" in ml.columns:
        bad = sorted(set(ml["trend_label"].astype(str).unique()) - allowed_labels)
        if bad:
            fail(f"ml: unexpected trend_label values: {bad}")

    # Aggregates should load
    monthly = pd.read_csv(MONTHLY_FILE)
    if "country" in monthly.columns:
        if (
            monthly["country"].astype(str) != monthly["country"].astype(str).str.upper()
        ).any():
            fail("monthly: country must be uppercase ISO-2")

    country_platform = pd.read_csv(COUNTRY_PLATFORM_FILE)
    if "country" in country_platform.columns:
        if (
            country_platform["country"].astype(str)
            != country_platform["country"].astype(str).str.upper()
        ).any():
            fail("country_platform: country must be uppercase ISO-2")

    # Quick consistency check: country_platform rows should be countries * platforms (usually 2)
    if {"country", "platform"}.issubset(country_platform.columns):
        dup = country_platform.duplicated(subset=["country", "platform"]).any()
        if dup:
            fail("country_platform: duplicate (country, platform) rows found")

    print("✅ Dataset validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
