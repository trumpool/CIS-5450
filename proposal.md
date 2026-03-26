# Project Proposal: U.S. Flight Delay Prediction

**CIS 5450: Big Data Analytics — Spring 2026**

---

## 1. Group Members & Duties

| Name | Responsibilities |
|------|-----------------|
| [Member 1] | Data acquisition (BTS flight data), data cleaning, data integration with weather data |
| [Member 2] | Exploratory Data Analysis (EDA), data visualization, geographic analysis |
| [Member 3] | Feature engineering, hypothesis testing, statistical analysis |
| [Member 4] | Model building, model evaluation, tuning, and final notebook compilation |

*Note: All members will collaborate on the final presentation and review each other's work throughout the project.*

---

## 2. Data Source

We will use two publicly available datasets:

**Primary Dataset: Bureau of Transportation Statistics (BTS) On-Time Performance Data**
- Source: https://www.transtats.bts.gov/DL_SelectFields.aspx?gnoyr_VQ=FGJ
- Coverage: All domestic U.S. flights for the year 2024 (approximately 6–7 million records)
- Key fields: flight date, airline, origin/destination airports, scheduled and actual departure/arrival times, delay duration, delay causes, distance, cancellation status, and tail number
- After filtering to the top 50 busiest airports and cleaning, we expect **5–6 million rows** with **20+ columns**, well exceeding the 50,000-row minimum

**Supplementary Dataset: NOAA Integrated Surface Database Lite (ISD-Lite)**
- Source: https://www.ncei.noaa.gov/pub/data/noaa/isd-lite/
- Coverage: Hourly weather observations at U.S. airports
- Key fields: air temperature, dew point, sea level pressure, wind direction, wind speed, cloud cover, and precipitation
- Airport IATA codes will be mapped to weather station IDs via the ISD station history file

Both datasets are free, publicly available, and published by U.S. government agencies.

---

## 3. Objective and Value Proposition

**Objective:** Build a predictive model that determines whether a U.S. domestic flight will be delayed by more than 15 minutes, using information available *before* departure — including flight scheduling details, airline and airport historical performance, weather conditions, and aircraft-level cascading delay effects.

**Why is this interesting?**

- Flight delays cost the U.S. economy over **$30 billion annually** (FAA estimates), affecting airlines, airports, and millions of passengers.
- Accurate delay prediction can help:
  - **Passengers** make smarter booking decisions and plan for disruptions
  - **Airlines** proactively allocate resources, rebook passengers, and reduce cascading delays
  - **Airports** optimize gate assignments and ground operations during high-risk periods
- This project integrates multiple big data concepts: large-scale data wrangling, multi-source data integration (flight + weather), time-series feature engineering, and scalable classification/regression modeling.

---

## 4. Modeling Plan

**Target Variable:**
- **Classification (primary):** `DepDel15` — binary indicator of whether departure delay exceeds 15 minutes (1 = delayed, 0 = on time)
- **Regression (secondary):** `DepDelay` — departure delay in minutes

**Feature Engineering Plan:**

| Feature Category | Examples |
|-----------------|----------|
| Temporal | Hour of day, day of week, month, holiday proximity, time-of-day bucket (morning/afternoon/evening/night) |
| Airline | Carrier identity, rolling 7-day airline delay rate |
| Airport | Origin airport daily flight volume, rolling 7-day airport delay rate, hub vs. non-hub indicator |
| Route | Origin-destination pair historical delay rate, flight distance |
| Weather | Temperature, wind speed, precipitation, cloud cover at origin and destination airports; composite weather severity score |
| Cascading | Previous flight arrival delay for the same aircraft (by tail number) |

*All historical rolling features will use a shift(1) strategy to prevent data leakage — only data from prior days will be used.*

**Models to Explore:**

| Model | Purpose |
|-------|---------|
| Logistic Regression | Baseline classifier; interpretable coefficients |
| Random Forest | Capture non-linear interactions; feature importance ranking |
| XGBoost / LightGBM | Best predictive performance; gradient boosting |
| Linear Regression | Baseline for delay duration regression |

**Evaluation Metrics:**
- Classification: Accuracy, Precision, Recall, F1-Score, AUC-ROC
- Regression: RMSE, MAE, R²

**Train/Test Split:** Temporal split (e.g., Jan–Oct 2024 for training, Nov–Dec 2024 for testing) to simulate real-world forecasting conditions. We will not use random splitting.

---

## 5. Hypothesis Testing

We plan to conduct the following hypothesis tests using simulation-based methods covered in class:

**Test 1: Low-Cost vs. Legacy Carriers**
- H₀: The mean departure delay of low-cost carriers (e.g., Spirit, Frontier) is equal to that of legacy carriers (e.g., Delta, United, American).
- H₁: The mean departure delay differs between the two groups.
- Method: Permutation test (10,000 permutations) on the difference in means.

**Test 2: Winter vs. Summer Delay Rates**
- H₀: The proportion of flights delayed >15 minutes is the same in winter (Dec–Feb) and summer (Jun–Aug).
- H₁: The delay proportions differ between seasons.
- Method: Bootstrap simulation to construct a confidence interval for the difference in proportions.

**Test 3: Hub vs. Non-Hub Airports**
- H₀: Hub airports and non-hub airports have the same average delay rate.
- H₁: Hub airports have a different delay rate than non-hub airports.
- Method: Permutation test on the difference in delay rates.

**Test 4: Weather Impact on Delays**
- H₀: The delay rate on days with adverse weather (precipitation > 5mm or wind speed > 10 m/s) is equal to the delay rate on clear-weather days.
- H₁: Adverse weather days have a higher delay rate.
- Method: Chi-square test with simulated p-value (Monte Carlo simulation, 10,000 iterations).

---

## 6. Anticipated Obstacles & Challenges

1. **Multi-source data integration:** Joining flight records with hourly weather observations requires careful spatial and temporal alignment — mapping airport codes to weather station IDs and matching weather readings to the nearest hour of scheduled departure.

2. **Data volume:** A full year of flight data contains 6–7 million rows. We may need to use chunked processing, sampling strategies, or optimized data types (e.g., `category` dtype in pandas) to work within memory constraints on Google Colab.

3. **Class imbalance:** Only ~20% of flights are delayed >15 minutes. We will explore techniques such as SMOTE, class weighting, and threshold tuning to address this imbalance.

4. **Data leakage prevention:** Many fields in the BTS dataset (e.g., actual departure time, delay cause breakdowns) are only available after the fact. We must be careful to exclude post-hoc features and use only information that would be available before departure.

5. **Missing data:** Weather observations may have gaps; delay cause fields are only populated for flights delayed 15+ minutes. We will need robust imputation or exclusion strategies.

6. **Cascading delay complexity:** Tracking aircraft-level delay propagation via tail numbers requires careful sorting and joining, and some tail number records may be missing or inconsistent.
