"""
Shared data bootstrap for CIS-5450 notebooks.

If `data/` is missing or incomplete, download the team dataset snapshot from Hugging Face.
Dataset layout matches local: `data/raw`, `data/processed`, `data/reports`.

Google Colab: open notebooks from a cloned repo (see repo README). Opening only one
`.ipynb` from GitHub leaves `project_data.py` off disk — run the README “Colab setup”
cell first so the runtime cwd is the repository root.

Env:
  FLIGHT_PROJECT_ROOT   - explicit repo root
  FLIGHT_DATA_DIR       - explicit data directory (default: <root>/data)
  HF_DATA_REPO_ID       - default: ahiruuu/CIS-5450
  FLIGHT_SKIP_HF        - if "1", never download (fail if data missing)
  FLIGHT_FORCE_HF       - if "1", re-download snapshot even if data looks ready
"""

from __future__ import annotations

import os
from pathlib import Path

DEFAULT_HF_DATASET = "ahiruuu/CIS-5450"


def resolve_project_root() -> Path:
    env_root = os.getenv("FLIGHT_PROJECT_ROOT")
    if env_root:
        return Path(env_root).expanduser().resolve()

    cwd = Path.cwd().resolve()
    for p in [cwd] + list(cwd.parents):
        if (p / "notebooks" / "project_data.py").exists():
            return p
        if (p / "notebooks").is_dir() and (p / "requirements.txt").is_file():
            return p
    return cwd


def _dir_nonempty(d: Path) -> bool:
    if not d.is_dir():
        return False
    try:
        next(d.iterdir())
    except StopIteration:
        return False
    return True


def data_layout_ready(data_root: Path) -> bool:
    """True if raw/processed/reports exist and each has at least one entry."""
    for name in ("raw", "processed", "reports"):
        if not _dir_nonempty(data_root / name):
            return False
    return True


def ensure_project_data(
    repo_id: str | None = None,
    *,
    force: bool | None = None,
) -> Path:
    """
    Ensure `<project>/data` exists with raw/processed/reports populated.
    Downloads from Hugging Face when needed.
    """
    repo_id = repo_id or os.getenv("HF_DATA_REPO_ID", DEFAULT_HF_DATASET)
    if force is None:
        force = os.getenv("FLIGHT_FORCE_HF", "0") == "1"

    if os.getenv("FLIGHT_SKIP_HF", "0") == "1":
        root = resolve_project_root()
        data_root = Path(os.getenv("FLIGHT_DATA_DIR", root / "data")).expanduser().resolve()
        if not data_layout_ready(data_root):
            raise FileNotFoundError(
                f"Data not ready at {data_root} and FLIGHT_SKIP_HF=1 (no HF download)."
            )
        print(f"[data] Using existing data (FLIGHT_SKIP_HF=1): {data_root}")
        return data_root

    root = resolve_project_root()
    data_root = Path(os.getenv("FLIGHT_DATA_DIR", root / "data")).expanduser().resolve()

    if not force and data_layout_ready(data_root):
        print(f"[data] Already present: {data_root}")
        return data_root

    try:
        from huggingface_hub import snapshot_download
    except ImportError as e:
        raise ImportError(
            "Install huggingface_hub: pip install huggingface_hub"
        ) from e

    data_root.mkdir(parents=True, exist_ok=True)
    print(f"[data] Downloading dataset '{repo_id}' -> {data_root} ...")
    snapshot_download(
        repo_id=repo_id,
        repo_type="dataset",
        local_dir=str(data_root),
        local_dir_use_symlinks=False,
    )
    print(f"[data] Ready: {data_root}")
    return data_root
