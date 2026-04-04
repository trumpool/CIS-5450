## 选题：美国航班延误预测

### 数据源
- **主数据**: BTS On-Time Performance（https://www.transtats.bts.gov/DL_SelectFields.aspx?gnoyr_VQ=FGJ）
  - 按月下载 CSV，每月约 50-60 万条，每年约 600-700 万条
  - 建议取 2024 完整一年 + 前50大机场，约 500-600 万行
- **辅助数据**: NOAA ISD-Lite 天气数据（https://www.ncei.noaa.gov/pub/data/noaa/isd-lite/）
  - 通过 isd-history.txt 映射机场 IATA 代码到气象站 ID
  - 按机场+最近整点与航班数据 join

### 分析计划
1. 数据获取与清洗 → 2. 特征工程 → 3. EDA → 4. 假设检验 → 5. 建模

### 特征工程方案
- **时间特征**: 小时、星期几、月份、出发时段分桶、是否周末、是否节假日、是否暑期
- **航空公司特征**: 过去7天平均延误率（shift(1)防泄漏）
- **机场特征**: 当日航班量、过去7天延误率、是否枢纽机场
- **航线特征**: 航线历史延误率、航线距离分桶
- **天气特征**: 出发/到达机场温度、风速、降水，天气严重程度评分，最差天气取值
- **连锁特征**: 同一飞机前序航班到达延误（最强特征之一）

### 建模方向
- 分类（是否延误>15分钟）: Logistic Regression → Random Forest → XGBoost
- 回归（延误分钟数）: Linear Regression
- 评估：Accuracy、F1、AUC-ROC（分类）；RMSE、MAE（回归）
- Train/Test 按时间切分，不随机 split

### 假设检验
- 廉价 vs 传统航空延误率（Permutation test）
- 冬季 vs 夏季延误率（Bootstrap simulation）
- 枢纽 vs 非枢纽机场（Permutation test）
- 恶劣天气 vs 晴天（Chi-square + simulation）
