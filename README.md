# CIS-5450 — Flight delay project

Onboarding for local Jupyter and **Google Colab**. Post-ingest notebooks use **Step 0** (`ensure_project_data()`) to fill `data/` from a local tree or the [team Hugging Face dataset](https://huggingface.co/datasets/ahiruuu/CIS-5450).

More detail: [huggingface_data_guide.md](huggingface_data_guide.md). Schedule and owners: [timeline.md](timeline.md).

## Quick start

### Local machine

1. Clone the repo and work with the repo folder as your project.
2. Create a venv, then: `pip install -r requirements.txt`
3. Run notebooks from any subfolder — `notebooks/project_data.py` finds the repo by walking parents from the current working directory.
4. In each notebook from `01` onward, run **Step 0** before loading data files.

### Google Colab

Colab’s default cwd is `/content`. If you open a notebook **from GitHub**, only that file is available unless you clone the repository, so **Step 0 cannot import `project_data.py` yet.** Run the following **once per new runtime**, **before** Step 0 (use your fork URL if it is not the canonical remote):

```python
import os, subprocess, sys
from pathlib import Path

REPO_URL = "https://github.com/trumpool/CIS-5450.git"
ROOT = Path("/content/CIS-5450")

if not (ROOT / "notebooks" / "project_data.py").exists():
    subprocess.run(["git", "clone", "--depth", "1", REPO_URL, str(ROOT)], check=True)

os.chdir(ROOT)
subprocess.check_call([sys.executable, "-m", "pip", "install", "-q", "-r", "requirements.txt"])
```

Then either:

- Continue in this notebook (after `os.chdir`, Step 0 will resolve paths correctly), or  
- Open the same notebook from **Runtime → files →** `CIS-5450/notebooks/...` so your place in the tree matches the repo.

**Optional — persist `data/` on Drive** (avoids re-downloading the HF snapshot when the runtime restarts):

```python
import os
from google.colab import drive

drive.mount("/content/drive")
os.environ["FLIGHT_DATA_DIR"] = "/content/drive/MyDrive/CIS-5450-data"  # create folder if needed
```

The next `ensure_project_data()` will use that directory (see [huggingface_data_guide.md](huggingface_data_guide.md) for `FLIGHT_DATA_DIR`).

## Folders

| Path | Purpose |
|------|---------|
| **`notebooks/00_data_ingest/`** | Download raw BTS flights and NOAA weather; writes under `data/raw/`. Use when rebuilding from sources instead of the HF snapshot. |
| **`notebooks/01_data_process/`** | Clean BTS and process weather into hourly tables; reads `data/raw/`, writes `data/processed/bts/`, `data/processed/weather/`, and QC under `data/reports/`. |
| **`notebooks/02_data_integration/`** | Join cleaned flights with weather; reads processed BTS + weather, writes `data/processed/integrated/` and join-quality reports under `data/reports/integrated/`. |
| **`notebooks/03_eda/`** | Exploratory analysis on cleaned or integrated data (depends on the notebook). |
| **`notebooks/project_data.py`** | Shared helpers: `ensure_project_data()`, `resolve_project_root()`. Import from notebooks (Step 0 adds `notebooks/` to `sys.path`). |
| **`data/raw/`** | Immutable-ish inputs: monthly flight parquets, weather extracts, station maps. |
| **`data/processed/`** | Pipeline outputs: `bts/` (e.g. cleaned flights), `weather/` (hourly weather), `integrated/` (flights + weather after join). |
| **`data/reports/`** | Side outputs: cancelled flights, extremes, missingness summaries, join diagnostics — not the main modeling tables. |
| **`docs/`** | Project briefs and planning (`requirement.md`, `proposal.md`, etc.). Not required to run the pipeline. |

## Notebook order (typical)

`00_data_ingest` → `01_data_process` → `02_data_integration` → `03_eda`

Skip `00` if your `data/` already matches the team snapshot (Step 0 can populate it from Hugging Face).

## Environment variables (optional)

Override defaults when needed; full table in [huggingface_data_guide.md](huggingface_data_guide.md).

- `HF_DATA_REPO_ID` — dataset id (default team repo on Hugging Face).
- `FLIGHT_DATA_DIR` — custom `data` directory (local path or Colab Drive path).
- `FLIGHT_PROJECT_ROOT` — explicit repo root (rarely needed if cwd is correct).
- `FLIGHT_SKIP_HF=1` — never download; fail if data missing.
- `FLIGHT_FORCE_HF=1` — re-download snapshot even if `data/` looks ready.
