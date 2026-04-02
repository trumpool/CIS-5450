# 项目任务时间线（内部使用）

**目标：4月17日 Check-in 前完成 数据清洗 + EDA + 基线模型 + 假设检验初稿**

---

## 总览

| 阶段 | 时间 | 负责人 |
|------|------|--------|
| 数据下载与初步检查 | 4.2 – 4.4 | Yihong + Yanchen |
| 数据清洗 | 4.4 – 4.7 | Yihong |
| 天气数据整合 | 4.4 – 4.8 | Yanchen |
| 特征工程 | 4.7 – 4.10 | Yanchen + Xiaoyang |
| EDA + 可视化 | 4.5 – 4.11 | Dong |
| 假设检验 | 4.9 – 4.13 | Dong |
| 基线模型 | 4.10 – 4.14 | Xiaoyang |
| Check-in 准备 | 4.15 – 4.16 | 全员 |
| **Check-in 会议** | **4.13 – 4.17** | **全员** |

---

## 详细任务

### Week 1（4.2 – 4.7）：数据基础

**Yihong Yu — 数据清洗**
- [ ] 4.2-4.3：确认 12 个月 parquet 文件全部下载完整（共 7,079,061 行）
- [ ] 4.4：处理缺失值 — `DepDelay`、`ArrDelay` 缺失行（已取消航班）单独标记，不直接删除
- [ ] 4.5：去除异常值（延误 > 600 分钟视为异常，单独记录）
- [ ] 4.6：统一数据类型（`FlightDate` 转 datetime，时间字段转 int）
- [ ] 4.7：输出清洗后的 `flights_2024_clean.parquet`，记录清洗前后行数

**Yanchen Zhou — 天气数据整合**
- [ ] 4.2-4.3：从 NOAA ISD-Lite 下载前 50 大机场 2024 年天气数据
- [ ] 4.4：用 isd-history.txt 建立 IATA ↔ 气象站ID 映射表
- [ ] 4.5-4.6：按 `Origin + 最近整点` join 出发机场天气；按 `Dest + 最近整点` join 到达机场天气
- [ ] 4.7：处理天气缺失值（线性插值或前向填充）
- [ ] 4.8：输出合并后的 `flights_2024_weather.parquet`

**Dong Dong — EDA 启动**
- [ ] 4.5：加载清洗数据，产出基本统计（延误率、各月分布、航空公司对比）
- [ ] 4.6-4.7：画出延误率按小时/星期/月份的分布图

---

### Week 2（4.8 – 4.14）：特征 + 分析 + 建模

**Yanchen Zhou + Xiaoyang Wan — 特征工程**
- [ ] 4.8-4.9：时间特征（hour、day_of_week、is_weekend、is_holiday、time_block）
- [ ] 4.9-4.10：历史滚动特征（airline/airport/route 过去7天延误率，注意 shift(1) 防泄漏）
- [ ] 4.10：连锁延误特征（同一架飞机 tail_number 前序航班到达延误）
- [ ] 4.11：输出最终特征矩阵 `features_2024.parquet`，附特征说明文档

**Dong Dong — EDA 深化 + 假设检验**
- [ ] 4.8-4.10：完成 EDA 核心图表（目标：3-5 张高质量图）
  - 地理热力图：各机场延误率
  - 天气与延误的散点图/箱线图
  - 航空公司延误对比图
  - 连锁延误效应图（前序延误 vs 当班延误）
- [ ] 4.11-4.12：实现假设检验
  - 廉价 vs 传统航空：Permutation test（10,000次）
  - 冬季 vs 夏季：Bootstrap simulation
  - 枢纽 vs 非枢纽：Permutation test
  - 恶劣天气 vs 晴天：Monte Carlo chi-square
- [ ] 4.13：整理检验结果，写出每个检验的结论段落

**Xiaoyang Wan — 基线模型**
- [ ] 4.10：加载 `features_2024.parquet`，按时间切分 train（1-10月）/ test（11-12月）
- [ ] 4.11：训练 Logistic Regression 基线，记录 Accuracy、F1、AUC-ROC
- [ ] 4.12-4.13：训练 Random Forest，对比基线
- [ ] 4.14：产出模型对比表，记录各模型指标

---

### Check-in 准备（4.15 – 4.16）

**全员**
- [ ] 4.15：汇总各自模块进度，整合进同一个 notebook
- [ ] 4.15：确认 notebook 可以从头到尾跑通
- [ ] 4.16：准备 Check-in 要汇报的内容（完成了什么、遇到了什么问题、接下来的计划）
- [ ] 4.16：与 TA 确认 Check-in 具体时间（4.13-4.17 之间）

---

## Check-in 后（4.17 – 4.28）

| 任务 | 负责人 | 截止 |
|------|--------|------|
| XGBoost / LightGBM 模型 | Xiaoyang | 4.21 |
| 类别不平衡处理（SMOTE / 权重调整） | Xiaoyang | 4.22 |
| Notebook 最终整合与注释 | 全员 | 4.25 |
| 演讲 PPT 制作 | 全员 | 4.26 |
| 录制 8-10 分钟演讲视频 | 全员 | 4.27 |
| Gradescope 提交（含添加队友） | 指定一人 | **4.28 11:59 PM** |

---

## 注意事项

- 每完成一个 parquet 输出节点，发到群里共享，确保大家用同一份数据
- 特征工程完成前，Dong 和 Xiaoyang 可以先用原始数据跑，等特征矩阵出来后替换
- Google Colab 不能同时编辑，各自在独立 notebook 里做，最后由一人合并
- 每次重新提交 Gradescope 记得重新添加队友（否则全队扣5分）
