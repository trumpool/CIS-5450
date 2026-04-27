# CIS 5450 Final Project — Flight Delay Prediction
# CIS 5450 期末项目 — 航班延误预测

**Team**: Xiaoyang Wan · Dong Dong · Yihong Yu · Yanchen Zhou
**Deadline**: 2026-04-28 11:59 PM EST
**Repo**: https://github.com/trumpool/CIS-5450

---

## 📊 项目一句话总结

用 2024 年全年 BTS 航班数据（680 万行）+ NOAA 小时级天气数据，建模预测美国国内航班是否会延误 ≥15 分钟。最佳模型 **AUC = 0.82, F1 = 0.59**。

---

## ✅ 提交进度盘点

| 交付物 | 状态 | 文件位置 |
|---|---|---|
| Proposal（5 分） | ✅ 已交 | [`docs/proposal.md`](docs/proposal.md) |
| 中期 Check-in（5 分） | ✅ 已开 | [`docs/archive/checkin_report.md`](docs/archive/checkin_report.md) |
| **Deliverable 1：主 Notebook（93 分）** | ✅ 已完成 | [`notebooks/CIS5450_final_project.ipynb`](notebooks/CIS5450_final_project.ipynb) |
| **Deliverable 3：难度概念 Notebook** | ✅ 已完成 | [`notebooks/CIS5450_difficulty_concepts.ipynb`](notebooks/CIS5450_difficulty_concepts.ipynb) |
| 演讲讲稿 + 高清图 | ✅ 已准备 | [`slides/PRESENTATION_SCRIPT.md`](slides/PRESENTATION_SCRIPT.md) |
| **Deliverable 2：8–10 分钟演讲视频** | ⚠️ **待录制** | — |
| **Deliverable 2：PDF 幻灯片** | ⚠️ **待制作** | — |
| **Gradescope 提交（含队友）** | ⚠️ **待操作** | — |

---

## ⏰ 截止前的 TODO

### 🔴 必须完成（4/28 之前）

1. **做 PPT**（推荐周末做，2-3 小时）
   - 按 [`slides/PRESENTATION_SCRIPT.md`](slides/PRESENTATION_SCRIPT.md) 里的 14 张幻灯片结构
   - 6 张高清图在 [`slides/figs/`](slides/figs/) 已经生成（16:9 比例，200 DPI）
   - **不要写大段文字，不能放代码**
   - 导出 **PDF** 备用提交

2. **录制 8–10 分钟视频**（推荐 4/27 周一）
   - **演讲者必须露脸**（用 Loom / OBS / Zoom 录屏 + Webcam）
   - **真人声音**（禁用 TTS）
   - **8 ≤ 时长 ≤ 10 分钟**（超出范围扣 5 分）
   - 不需要全员讲话，但**全员要在画面中**
   - 讲稿 + timing 在 [`slides/PRESENTATION_SCRIPT.md`](slides/PRESENTATION_SCRIPT.md)

3. **Gradescope 三件套提交**（4/28 11:59 PM EST 之前）
   - 主 Notebook：[`notebooks/CIS5450_final_project.ipynb`](notebooks/CIS5450_final_project.ipynb)
   - 难度概念 Notebook：[`notebooks/CIS5450_difficulty_concepts.ipynb`](notebooks/CIS5450_difficulty_concepts.ipynb)
   - 视频 + PDF 幻灯片
   - ❗ **每次提交都要重新加队友**（漏加全队扣 5 分）

4. **填贡献评估 Google 表单**（每个人都要填）

---

## 📁 项目结构

```
CIS-5450/
├── README.md                              ← 本文件（队友入口）
├── requirements.txt                       ← pip install -r
├── huggingface_data_guide.md              ← 数据下载详细指南
│
├── notebooks/
│   ├── CIS5450_final_project.ipynb        ★ Deliverable 1：主提交 notebook
│   ├── CIS5450_difficulty_concepts.ipynb  ★ Deliverable 3：难度概念定位
│   ├── project_data.py                    ← 共享辅助：ensure_project_data()
│   │
│   ├── 00_data_ingest/                    ← 原始 BTS + NOAA 数据下载
│   ├── 01_data_process/                   ← 数据清洗（BTS + 天气）
│   ├── 02_data_integration/               ← 天气 join + 特征工程
│   ├── 03_eda/                            ← EDA + 假设检验
│   └── 04_modeling/                       ← 基线 / 高级 / 调优 / 全量 / 回归
│
├── slides/
│   ├── PRESENTATION_SCRIPT.md             ★ 完整讲稿 + 嵌入的图（14 张）
│   └── figs/                              ★ 6 张幻灯片专用高清图
│
├── data/
│   ├── raw/                               ← 原始数据（不入 git）
│   ├── processed/                         ← 中间产出（不入 git）
│   │   └── integrated/features_2024.parquet  ← 主特征表（680 万行）
│   └── reports/                           ← 可视化输出 + CSV 摘要
│       ├── eda/  hypothesis/  modeling/   bts/  weather/  integrated/
│
└── docs/
    ├── proposal.md                        ← 已提交的项目提案
    ├── requirement.md                     ← 官方项目要求（英文）
    ├── requirement_cn.md                  ← 中文翻译
    └── archive/                           ← 历史/中间文档（已归档）
```

---

## 📊 最终结果速查

### 分类（最佳模型：调阈值后的 XGBoost）

| Model | Accuracy | Precision | Recall | F1 | AUC-ROC |
|---|---|---|---|---|---|
| Naive (always on-time) | 0.821 | 0.000 | 0.000 | 0.000 | 0.500 |
| Logistic Regression | 0.810 | 0.471 | 0.512 | 0.490 | 0.757 |
| Random Forest | 0.854 | 0.600 | 0.543 | 0.570 | 0.806 |
| XGBoost (weighted) | 0.857 | 0.609 | 0.553 | 0.580 | 0.811 |
| LightGBM (weighted) | 0.850 | 0.582 | 0.573 | 0.578 | 0.815 |
| XGBoost + SMOTE | 0.878 | 0.809 | 0.415 | 0.549 | 0.813 |
| **XGBoost (tuned, t=0.566)** | **0.867** | **0.663** | **0.525** | **0.586** | **0.819** |

### 回归（最佳：LightGBM Regressor）

| Model | RMSE | MAE | R² |
|---|---|---|---|
| Naive (predict mean) | 37.95 | 21.24 | -0.006 |
| Linear Regression | 34.79 | 16.49 | 0.154 |
| Ridge Regression | 34.79 | 16.49 | 0.154 |
| **LightGBM Regressor** | **32.41** | **13.60** | **0.266** |

### 假设检验（4 项全部拒绝 H₀，α=0.05）

| # | Question | Method | Effect | p |
|---|---|---|---|---|
| 1 | Budget vs. Legacy carriers | Permutation (B=10k) | +5.4 pp | <0.0001 |
| 2 | Summer vs. Winter | Bootstrap CI | −5.8 pp | <0.0001 |
| 3 | Hub vs. Non-hub | Permutation (B=10k) | +1.9 pp | <0.0001 |
| 4 | Bad Weather vs. Clear | Monte Carlo χ² | χ²=15,009 | <0.0001 |

---

## 🔧 本地运行

### 安装

```bash
git clone https://github.com/trumpool/CIS-5450.git
cd CIS-5450
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# macOS only — XGBoost 需要 OpenMP
brew install libomp
```

### 数据准备

数据通过 Hugging Face 同步：[ahiruuu/CIS-5450](https://huggingface.co/datasets/ahiruuu/CIS-5450)

每个 notebook 第一段 `ensure_project_data()` 会自动从 HF 拉取需要的数据。
详见 [`huggingface_data_guide.md`](huggingface_data_guide.md)。

### 运行主 notebook

```bash
jupyter notebook notebooks/CIS5450_final_project.ipynb
```

主 notebook 加载缓存的 `features_2024.parquet`，端到端运行 EDA + 假设检验 + 建模。

### 重新生成完整管线

如果想从原始数据完全重跑（耗时较长）：

```
notebooks/00_data_ingest  →  notebooks/01_data_process  →  notebooks/02_data_integration
```

然后再跑 `03_eda` 和 `04_modeling`。

---

## 🌐 Google Colab

Colab 默认 cwd 是 `/content`。如果直接从 GitHub 打开 notebook，**先运行下面这段**再运行 Step 0：

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

**可选 — 把 `data/` 持久化到 Drive**（避免每次重启都重新下载）：

```python
import os
from google.colab import drive

drive.mount("/content/drive")
os.environ["FLIGHT_DATA_DIR"] = "/content/drive/MyDrive/CIS-5450-data"
```

---

## ⚙️ 环境变量（可选）

| 变量 | 含义 |
|---|---|
| `HF_DATA_REPO_ID` | HF 数据集 ID（默认团队仓库） |
| `FLIGHT_DATA_DIR` | 自定义 `data` 目录（本地或 Drive 路径） |
| `FLIGHT_PROJECT_ROOT` | 显式指定仓库根目录 |
| `FLIGHT_SKIP_HF=1` | 永不从 HF 下载，缺数据则报错 |
| `FLIGHT_FORCE_HF=1` | 强制重新下载 HF 快照 |

---

## 📚 关键文档索引

| 文件 | 用途 |
|---|---|
| [`README.md`](README.md) | 本文件（队友入口） |
| [`notebooks/CIS5450_final_project.ipynb`](notebooks/CIS5450_final_project.ipynb) | 主提交 notebook（93 分） |
| [`notebooks/CIS5450_difficulty_concepts.ipynb`](notebooks/CIS5450_difficulty_concepts.ipynb) | 难度概念定位 notebook |
| [`slides/PRESENTATION_SCRIPT.md`](slides/PRESENTATION_SCRIPT.md) | 演讲讲稿 + 嵌入图 |
| [`docs/proposal.md`](docs/proposal.md) | 提交过的 proposal |
| [`docs/requirement.md`](docs/requirement.md) | 官方项目要求 |
| [`docs/requirement_cn.md`](docs/requirement_cn.md) | 项目要求中文翻译 |
| [`huggingface_data_guide.md`](huggingface_data_guide.md) | HF 数据下载详细指南 |
| [`docs/archive/`](docs/archive/) | 历史 / 中间文档（已归档） |
