# CIS 5450 Final Project — Submission Guide
# CIS 5450 期末项目 — 提交指南

**Team**: Xiaoyang Wan · Dong Dong · Yihong Yu · Yanchen Zhou
**Project**: U.S. Flight Delay Prediction (2024 BTS + NOAA)
**Date**: April 28, 2026

---

## 1. Deliverables / 交付物清单

### Deliverable 1 — Annotated Notebook (93 pts)

**Primary file**: [`notebooks/CIS5450_final_project.ipynb`](notebooks/CIS5450_final_project.ipynb)

一个综合 Notebook，包含完整的项目叙述：
- 背景介绍与研究问题
- 数据源说明（BTS + NOAA）
- 数据清洗与整合
- 特征工程（23 个特征，防泄漏设计）
- EDA（8 个关键可视化 + 解读）
- 四项假设检验（permutation / bootstrap / Monte Carlo）
- 分类建模（Naive → LR → RF → XGBoost → LightGBM → SMOTE → Tuned → Threshold Optimized）
- 回归建模（Linear / Ridge / LightGBM）
- 关键发现、挑战、未来方向

该 Notebook 加载缓存的 `features_2024.parquet` 然后端到端运行。79 个 cell。

### Deliverable 2 — Presentation (20 pts)

**To prepare / 待准备**:
- 8–10 min 幻灯片演讲（录像或现场）
- PDF 形式的 slides
- 内容：objective、dataset、3–5 张 EDA 图、modeling 结果、hypothesis tests、insights、challenges
- 要求：不要放代码、必须露脸、不能用 TTS

**Content outline / 建议结构**:
1. Problem & value proposition (1 min)
2. Dataset (1 min)
3. EDA highlights — 3 charts (2 min):
   - Cascading delay effect
   - Airline comparison (budget vs legacy)
   - Weather effect
4. Hypothesis testing results (1.5 min)
5. Modeling results + ROC (2 min)
6. Key insights & business value (1.5 min)
7. Challenges & future work (1 min)

### Deliverable 3 — Difficulty Concept Location Notebook

**File**: [`notebooks/CIS5450_difficulty_concepts.ipynb`](notebooks/CIS5450_difficulty_concepts.ipynb)

详细说明了 15 个难度概念在项目中的使用位置与原因。

---

## 2. Repository Structure / 仓库结构

```
CIS-5450/
├── SUBMISSION.md                      ← this file
├── README.md
├── requirements.txt                   ← pip install -r
├── checkin_report.md                  ← mid-term check-in (Apr 17)
├── docs/
│   ├── proposal.md                    ← original proposal
│   ├── requirement.md                 ← project spec
│   └── flight_delay_plan.md           ← planning doc
├── notebooks/
│   ├── CIS5450_final_project.ipynb         ★ main integrated notebook (Deliverable 1)
│   ├── CIS5450_difficulty_concepts.ipynb   ★ concept locator (Deliverable 3)
│   ├── 00_data_ingest/
│   │   ├── BTS_download.ipynb
│   │   └── weather_download.ipynb
│   ├── 01_data_process/
│   │   ├── BTS_cleaning.ipynb
│   │   └── weather_process.ipynb
│   ├── 02_data_integration/
│   │   ├── weather_join.ipynb
│   │   └── feature_engineering.ipynb
│   ├── 03_eda/
│   │   ├── eda.ipynb
│   │   └── hypothesis_testing.ipynb
│   └── 04_modeling/
│       ├── baseline_model.ipynb             (LR + RF)
│       ├── advanced_model.ipynb             (XGBoost + LightGBM + SMOTE)
│       ├── tuning_optimization.ipynb        (RandomizedSearchCV + threshold opt)
│       ├── regression_model.ipynb           (Linear + Ridge + LightGBM Regressor)
│       └── fulldata_final_model.ipynb       (full 5.6M row validation)
└── data/
    ├── raw/                           ← not committed (large)
    ├── processed/                     ← not committed
    └── reports/                       ← key figures & summary CSVs (committed)
        ├── bts/
        ├── weather/
        ├── integrated/
        ├── eda/
        ├── hypothesis/
        └── modeling/
```

---

## 3. Final Results / 最终结果

### Classification / 分类

**Target**: `DepDel15` (delayed ≥15 min)
**Split**: Jan–Oct 2024 train → Nov–Dec 2024 test

| Model | Accuracy | Precision | Recall | F1 | AUC-ROC |
|---|---|---|---|---|---|
| Naive (always on-time) | 0.821 | 0.000 | 0.000 | 0.000 | 0.500 |
| Logistic Regression | 0.817 | 0.488 | 0.476 | 0.482 | 0.755 |
| Random Forest | 0.853 | 0.598 | 0.545 | 0.571 | 0.804 |
| XGBoost (weighted) | 0.858 | 0.612 | 0.556 | 0.583 | 0.815 |
| LightGBM (weighted) | 0.851 | 0.585 | 0.574 | 0.580 | 0.817 |
| XGBoost + SMOTE | 0.878 | 0.809 | 0.418 | 0.551 | 0.814 |
| **XGBoost (tuned, t=0.566)** | **0.867** | **0.659** | **0.529** | **0.587** | **0.819** |

### Regression / 回归

**Target**: `DepDelay` (minutes)

| Model | RMSE | MAE | R² |
|---|---|---|---|
| Naive (predict mean) | 37.95 | 21.24 | -0.006 |
| Linear Regression | 34.80 | 16.52 | 0.154 |
| Ridge Regression | 34.80 | 16.52 | 0.154 |
| **LightGBM Regressor** | **32.47** | **13.62** | **0.263** |

### Hypothesis Tests / 假设检验 (all reject H₀ at α=0.05)

| # | Question | Method | Effect | p-value |
|---|---|---|---|---|
| 1 | Budget vs. Legacy airlines | Permutation (B=10k) | +5.40 pp | <0.0001 |
| 2 | Summer vs. Winter | Bootstrap CI (B=10k) | -5.79 pp | <0.0001 |
| 3 | Hub vs. Non-Hub | Permutation (B=10k) | +1.92 pp | <0.0001 |
| 4 | Bad Weather vs. Clear | Monte Carlo χ² (B=10k) | χ²=15,009 | <0.0001 |

---

## 4. Gradescope Submission Checklist

- [ ] Submit `CIS5450_final_project.ipynb` (Deliverable 1)
- [ ] Record 8-10 min video with slides (Deliverable 2)
- [ ] Upload presentation slides as PDF (Deliverable 2)
- [ ] Submit `CIS5450_difficulty_concepts.ipynb` (Deliverable 3)
- [ ] **Add all teammates on Gradescope** (re-add after every resubmission!)
- [ ] Verify all teammates receive grades

---

## 5. How to Run Locally

```bash
# Install dependencies
pip install -r requirements.txt

# Additional requirement for macOS (XGBoost)
brew install libomp

# Run the main notebook
cd notebooks/
jupyter notebook CIS5450_final_project.ipynb
```

The main notebook loads cached `features_2024.parquet` (produced by upstream notebooks).
To regenerate from raw data, run notebooks in order: `00_data_ingest → 01_data_process →
02_data_integration`.

---

## 6. Reproducibility Notes

- `RANDOM_STATE = 42` set at top of every notebook
- Stratified subsampling preserves class balance (~80:20)
- Temporal train/test split prevents information leakage
- All rolling features use `shift(1)` before rolling window
- XGBoost requires `libomp` on macOS (`brew install libomp`)
- SMOTE requires `float64` feature dtypes (cast explicitly)
