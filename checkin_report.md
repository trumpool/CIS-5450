# Check-in Report — Flight Delay Prediction
# 中期汇报 — 航班延误预测

**Team**: Xiaoyang Wan, Yihong Yu, Yanchen Zhou, Dong Dong
**Date**: April 17, 2026

---

## 1. What We've Completed / 已完成的工作

### 1.1 Data Collection & Cleaning / 数据采集与清洗

- Downloaded all 12 months of 2024 BTS on-time flight data (7,079,061 rows → 6,817,598 after cleaning)
  下载 BTS 2024 全年航班数据（清洗前 7,079,061 行 → 清洗后 6,817,598 行）

- Downloaded NOAA ISD-Lite hourly weather data for top 50 US airports
  下载 NOAA ISD-Lite 小时级天气数据（前 50 大机场）

- Missing values: cancelled flights flagged separately, not dropped; delays > 600 min marked as outliers
  缺失值处理：取消航班单独标记不删除；延误 > 600 分钟标为异常值

- Standardized dtypes (`FlightDate` → datetime, time fields → int)
  统一数据类型（FlightDate 转 datetime，时间字段转 int）

- Weather join: matched origin/destination airports to nearest-hour weather observations via `merge_asof`
  天气整合：按出发/到达机场 + 最近整点 join 天气数据

- Output: `flights_2024_clean.parquet`, `flights_2024_weather.parquet`

### 1.2 Feature Engineering / 特征工程

23 new features across 8 categories / 8 大类 23 个新特征：

| Category / 类别 | Features / 特征 |
|---|---|
| Time / 时间 | `dep_hour`, `day_of_week`, `is_weekend`, `time_block` |
| Holiday / 节假日 | `is_holiday`, `holiday_proximity` |
| Hub & Distance / 枢纽与距离 | `is_origin_hub`, `is_dest_hub`, `distance_bin` |
| Rolling History / 滚动历史 | `airline_delay_rate_7d`, `origin_delay_rate_7d`, `route_delay_rate_7d` (with `shift(1)` to prevent leakage / 用 shift(1) 防止数据泄漏) |
| Cascading Delay / 连锁延误 | `prev_flight_arr_delay` (same aircraft's prior flight / 同架飞机前序航班延误) |
| Aircraft Utilization / 机队利用率 | `tail_leg_today` |
| Congestion / 拥堵度 | `origin_hourly_flights` |
| Weather Interactions / 天气交互 | `origin_freezing_rain`, `origin_wind_rain`, `origin_fog_risk` (+ dest equivalents) |

Output: `features_2024.parquet` (81 columns, 6,817,598 rows)

### 1.3 EDA / 探索性数据分析

~25 visualizations including / 约 25 张可视化图表，包括：
- Delay rate by hour / weekday / month / 延误率按小时、星期、月份分布
- Airline comparison / 航空公司延误率对比
- Airport geographic heatmap / 机场地理热力图
- Weather vs. delay scatter/box plots / 天气与延误散点图/箱线图
- Cascading delay effect (prior delay vs. current delay) / 连锁延误效应图
- Congestion and aircraft utilization impact / 拥堵度与机队利用率影响

### 1.4 Hypothesis Testing / 假设检验

All four tests reject H₀ at α = 0.05 / 四项检验均在 α=0.05 下拒绝原假设：

| # | Question / 问题 | Method / 方法 | Effect / 效应 | p-value |
|---|---|---|---|---|
| 1 | Budget vs. legacy airlines / 廉价 vs 传统航空 | Permutation test (10,000) | +5.40 pp | < 0.0001 |
| 2 | Winter vs. summer / 冬季 vs 夏季 | Bootstrap CI (10,000) | −5.79 pp | < 0.0001 |
| 3 | Hub vs. non-hub airports / 枢纽 vs 非枢纽机场 | Permutation test (10,000) | +1.92 pp | < 0.0001 |
| 4 | Bad weather vs. clear / 恶劣天气 vs 晴天 | Monte Carlo χ² (10,000) | χ² = 15,009 | < 0.0001 |

### 1.5 Modeling / 建模

Binary classification target: `DepDel15` (delayed ≥ 15 min)
二分类目标：DepDel15（延误 ≥ 15 分钟）

Temporal split: train on Jan–Oct, test on Nov–Dec (prevents future leakage)
时间切分：1–10 月训练，11–12 月测试（防止未来信息泄漏）

| Model / 模型 | Accuracy | Precision | Recall | F1 | AUC-ROC |
|---|---|---|---|---|---|
| Naive (always on-time) / 朴素基线 | 0.821 | 0.000 | 0.000 | 0.000 | 0.500 |
| Logistic Regression / 逻辑回归 | 0.817 | 0.488 | 0.476 | 0.482 | 0.755 |
| Random Forest / 随机森林 | 0.853 | 0.598 | 0.545 | 0.571 | 0.804 |
| XGBoost (class-weighted) | 0.858 | 0.612 | 0.556 | 0.583 | 0.815 |
| **LightGBM (class-weighted)** | **0.851** | **0.585** | **0.574** | **0.580** | **0.817** |
| XGBoost + SMOTE | 0.878 | 0.809 | 0.418 | 0.551 | 0.814 |
| LightGBM + SMOTE | 0.878 | 0.797 | 0.424 | 0.554 | 0.815 |

Best model: **LightGBM (class-weighted)** — AUC-ROC = 0.817
最佳模型：LightGBM（类别加权）— AUC-ROC = 0.817

---

## 2. Key Findings / 关键发现

1. **Cascading delay is the strongest predictor / 连锁延误是最强预测因子**
   `prev_flight_arr_delay` has 0.50 Gini importance in Random Forest — whether the same aircraft's previous flight was delayed dominates all other features.
   同架飞机前序航班延误在随机森林中的重要性高达 0.50，远超其他特征。

2. **Class weights outperform SMOTE / 类别权重优于 SMOTE**
   SMOTE dramatically boosts precision (0.80+) but sacrifices recall (0.42). Built-in class weights achieve better recall and comparable AUC.
   SMOTE 大幅提升精确率（0.80+）但牺牲召回率（0.42）。内置类别权重在召回率和 AUC 上表现更优。

3. **Summer delays more than winter (counterintuitive) / 夏季延误多于冬季（反直觉）**
   Summer delay rate is 5.8 pp higher than winter — likely due to thunderstorm season and peak travel volume.
   夏季延误率比冬季高 5.8 个百分点，可能因雷暴季节和暑期客流高峰。

4. **Budget carriers delay significantly more / 廉价航空延误显著更多**
   Frontier, Spirit, Allegiant have 5.4 pp higher delay rate than Delta, American, United.
   Frontier、Spirit、Allegiant 的延误率比 Delta、American、United 高 5.4 个百分点。

---

## 3. Challenges / 遇到的问题

| Challenge / 问题 | Solution / 解决方案 |
|---|---|
| Dataset too large (6.8M rows) for standard sklearn solvers — LogisticRegression timed out after 30 min / 数据量太大，LogisticRegression 超时 | Switched to SGDClassifier + stratified subsampling (1M rows) / 改用 SGDClassifier + 分层抽样 |
| Class imbalance (~80:20 on-time vs delayed) / 类别不平衡 | Compared SMOTE vs class_weight="balanced"; class weights performed better / 对比 SMOTE 与类别权重，后者更优 |
| SMOTE incompatible with pandas nullable Int64 dtype / SMOTE 与 pandas 可空整数类型不兼容 | Cast all features to float64 before resampling / 统一转换为 float64 |
| XGBoost requires OpenMP on macOS / XGBoost 在 macOS 需要 OpenMP | `brew install libomp` |
| Weather data join required temporal alignment / 天气数据需要时间对齐 | Used `merge_asof` with nearest-hour matching / 使用 merge_asof 按最近整点匹配 |

---

## 4. Next Steps / 接下来的计划

| Task / 任务 | Deadline / 截止 |
|---|---|
| Hyperparameter tuning (GridSearch / Optuna) / 超参数调优 | Apr 21 |
| Threshold optimization (precision-recall tradeoff) / 阈值优化 | Apr 22 |
| Final notebook integration with Markdown annotations / Notebook 最终整合与注释 | Apr 25 |
| Difficulty concept locator notebook / 难度概念定位 Notebook | Apr 25 |
| Presentation slides / 演讲 PPT | Apr 26 |
| Record 8–10 min video / 录制演讲视频 | Apr 27 |
| **Gradescope submission / 提交** | **Apr 28 11:59 PM** |

---

## 5. Notebook Structure / Notebook 结构

| Notebook | Location / 路径 | Description / 说明 |
|---|---|---|
| Data download | `00_data_ingest/` | BTS + NOAA raw data |
| Data cleaning | `01_data_process/BTS_cleaning.ipynb` | 7M → 6.8M rows |
| Weather processing | `01_data_process/weather_process.ipynb` | ISD-Lite parsing |
| Weather join | `02_data_integration/weather_join.ipynb` | Flight ⟕ weather |
| Feature engineering | `02_data_integration/feature_engineering.ipynb` | 23 new features |
| EDA | `03_eda/eda.ipynb` | ~25 visualizations |
| Hypothesis testing | `03_eda/hypothesis_testing.ipynb` | 4 simulation-based tests |
| Baseline models | `04_modeling/baseline_model.ipynb` | LR + Random Forest |
| Advanced models | `04_modeling/advanced_model.ipynb` | XGBoost + LightGBM + SMOTE |
