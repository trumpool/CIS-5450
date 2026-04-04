# Hugging Face Data Repo

**Default team dataset:** [ahiruuu/CIS-5450](https://huggingface.co/datasets/ahiruuu/CIS-5450) (layout: `raw/`, `processed/`, `reports/` at repo root — mirrors local `data/raw`, `data/processed`, `data/reports`).

## Single source of truth in notebooks (use this first)

| What | Where |
|------|--------|
| **Canonical behavior** | `notebooks/project_data.py` — `ensure_project_data()` + `resolve_project_root()` |
| **When it runs** | **Step 0** in post-ingest notebooks (before any paths / loads) |

You do **not** need to paste separate Hugging Face snippets into those notebooks: Step 0 already downloads the full dataset snapshot into `data/` when needed (via `snapshot_download`).

**This guide** below adds: folder layout reference, env vars (same ones `project_data.py` reads), and **optional** copy-paste patterns for scripts or one-off partial downloads — not a second parallel workflow inside the same notebook.

## Automatic setup in notebooks (details)

Post-ingest notebooks call `ensure_project_data()` from `notebooks/project_data.py` in **Step 0**. If `data/` is missing or empty, it runs `snapshot_download` into your repo’s `data/` folder so teammates can open any notebook without manual downloads.

### Google Colab

Colab runtimes start in `/content` and **do not** include the rest of the repo when you open a single notebook from GitHub, so `project_data.py` is missing until you clone. Use the **Colab setup** cell in [README.md](README.md) once per runtime (clone → `chdir` → `pip install`), then run **Step 0** as usual. The public team dataset does not require `huggingface-cli login`; set a [HF token](https://huggingface.co/docs/hub/security-tokens) only if you switch to a private dataset or hit rate limits.

Environment variables:

| Variable | Purpose |
|----------|---------|
| `HF_DATA_REPO_ID` | Override dataset (default `ahiruuu/CIS-5450`) |
| `FLIGHT_SKIP_HF` | Set to `1` to never download (fails if data not present) |
| `FLIGHT_FORCE_HF` | Set to `1` to re-download even if `data/` looks populated |
| `FLIGHT_PROJECT_ROOT` | Explicit repo root |
| `FLIGHT_DATA_DIR` | Explicit data directory (default `<root>/data`) |

---

Use a Hugging Face **dataset** repo with this structure:

```text
raw/
  bts/
    flights_2024_01.parquet
    ...
    flights_2024_12.parquet
    monthly_counts_2024.csv
  weather/
    weather_2024_isd_lite_raw.parquet
    weather_station_map_top50_2024.csv

processed/
  bts/
    flights_2024_clean.parquet
  weather/
    weather_2024_hourly.parquet
  integrated/
    flights_2024_weather.parquet
    # later
    features_2024.parquet

reports/
  bts/
    bts_cleaning_summary_2024.csv
  weather/
    weather_download_summary_2024.csv
    weather_process_missingness_2024.csv
  integrated/
    weather_join_quality_2024.csv
```

If repo size becomes too large, split into two dataset repos:
- `...-raw` (raw data)
- `...-processed` (processed + reports, most teammates only need this)

## Optional: manual retrieval (scripts / one-off / no Step 0)

Use the snippets below only when you are **not** relying on Step 0 + `project_data.py` — for example a standalone script, a partial download, or a quick experiment in a scratch notebook.

## Team retrieval patterns (copy-paste)

Install:

```bash
pip install huggingface_hub
```

### A) Download one file (optional; skip if you use Step 0)

```python
from huggingface_hub import hf_hub_download
import pandas as pd

REPO_ID = "ahiruuu/CIS-5450"

path = hf_hub_download(
    repo_id=REPO_ID,
    repo_type="dataset",
    filename="processed/integrated/flights_2024_weather.parquet",
)

df = pd.read_parquet(path)
print(df.shape)
```

### B) Download only a folder subset (avoid full clone)

```python
from huggingface_hub import snapshot_download

REPO_ID = "ahiruuu/CIS-5450"

local_dir = snapshot_download(
    repo_id=REPO_ID,
    repo_type="dataset",
    allow_patterns=[
        "processed/integrated/*",
        "reports/integrated/*",
    ],
)

print(local_dir)
```

## Local file vs single-file download (advanced)

If you already ran **Step 0**, read from disk:

`data/processed/integrated/flights_2024_weather.parquet`

If you need **only one file** from Hugging Face (e.g. tiny Colab test) without full `snapshot_download`, you can use `hf_hub_download` — this is **not** what `project_data.py` uses; it duplicates behavior only if you skip Step 0 on purpose:

```python
import os
from huggingface_hub import hf_hub_download

HF_REPO_ID = os.getenv("HF_DATA_REPO_ID", "ahiruuu/CIS-5450")

flights_path = hf_hub_download(
    repo_id=HF_REPO_ID,
    repo_type="dataset",
    filename="processed/integrated/flights_2024_weather.parquet",
)
print("Cached file:", flights_path)
```