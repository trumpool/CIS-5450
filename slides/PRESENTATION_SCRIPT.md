# Presentation Script — U.S. Flight Delay Prediction
# 演讲讲稿 — 航班延误预测

**Total target time**: ~9:15 (under 10 min)
**Slides**: 23 (deck.html)
**Speaking rate**: ~150 wpm assumed

---

## ⏱ Timing Plan

| # | Slide | Target | Cumulative |
|---|---|---|---|
| 1 | Cover | 0:15 | 0:15 |
| 2 | The Problem ($30B) | 0:30 | 0:45 |
| 3 | Stakeholders | 0:25 | 1:10 |
| 4 | Dataset | 0:30 | 1:40 |
| 5 | Data Quality | 0:25 | 2:05 |
| 6 | Feature Engineering | 0:30 | 2:35 |
| 7 | Cascading Delay ⭐ | 0:50 | 3:25 |
| 8 | Temporal Patterns | 0:25 | 3:50 |
| 9 | Weather | 0:25 | 4:15 |
| 10 | Airline Reliability | 0:20 | 4:35 |
| 11 | Hypothesis Tests | 0:35 | 5:10 |
| 12 | Null Distributions | 0:20 | 5:30 |
| 13 | Modeling Approach | 0:30 | 6:00 |
| 14 | ROC Ladder | 0:25 | 6:25 |
| 15 | SMOTE vs Weighted | 0:20 | 6:45 |
| 16 | Hyperparameter Tuning | 0:20 | 7:05 |
| 17 | Threshold Tuning | 0:20 | 7:25 |
| 18 | Model Performance ⭐ | 0:50 | 8:15 |
| 19 | Feature Importance | 0:25 | 8:40 |
| 20 | Regression Detour | 0:25 | 9:05 |
| 21 | Insurance ROI ⭐ | 0:50 | 9:55 |
| 22 | Challenges & Future | 0:30 | 10:25 |
| 23 | Thanks | 0:10 | 10:35 |

> Buffer: targeting ~9:15 spoken, allowing ~45 s for transitions and pauses.

---

## 1 · Cover · 0:15

> "Hi, we're [team]. Our project is U.S. flight delay prediction — given everything you know before the gate, can we predict whether your flight will be late? Built on 6.8 million 2024 flight records joined with hourly weather. Let's go."

*(35 words)*

---

## 2 · The Problem ($30B) · 0:30

> "Last year, nearly one in five U.S. domestic flights was late by 15 minutes or more. The FAA puts the total cost at 30 billion dollars a year. But the real problem isn't the dollar number — delays cascade. One late flight blows a connection, displaces an aircraft, forces a crew swap. Our question: how well can we predict this *before* the gate?"

*(67 words)*

---

## 3 · Stakeholders · 0:25

> "Why does anyone care? Four stakeholders. Passengers — pick the reliable flight, buy delay insurance. Airlines — pre-position crews, reroute aircraft. Airports — pre-staff gates. And insurers — price delay insurance more accurately. We'll come back to that insurance angle with concrete ROI numbers."

*(48 words)*

---

## 4 · Dataset · 0:30

> "Two public datasets. BTS On-Time Performance — every U.S. domestic flight in 2024, 7 million raw rows, 6.8 million after cleaning. NOAA hourly weather at the 50 busiest airports. The tricky part is joining them — flights are minute-precise, weather is hourly. We used pandas `merge_asof` with a 2-hour tolerance. About 80% of flights at top-50 airports got a valid weather match."

*(67 words)*

---

## 5 · Data Quality · 0:25

> "About 80% of flights are on-time, 20% delayed at least 15 minutes. Heavy class imbalance — that's the central modeling challenge. Cleaning was a 7-step pipeline: ISD-Lite sentinel decoding, dropping diverted flights, removing 600-minute outliers, deduplication. End result: 96.3% retention — 6.82 million rows, 81 columns."

*(53 words)*

---

## 6 · Feature Engineering · 0:30

> "Twenty-three engineered features in eight categories. Two carry the model — cascading delays and time-of-day. The most important discipline is anti-leakage: every rolling stat uses `shift(1)` before the rolling window. Today's target never feeds today's feature. Drop the shift, CV-AUC silently inflates 5 to 6 percentage points — classic leakage."

*(57 words)*

---

## 7 · Cascading Delay ⭐ · 0:50

> "This is the most important chart of our project. X-axis: how late was the previous leg of the same aircraft. Y-axis: how often the next flight is delayed. When the prior leg was on-time or early — the green bars — only about 10% of next flights are delayed, below the 20% baseline. But when the prior leg was 30 to 60 minutes late, the next flight delay rate jumps to 59%. 60 to 120 minutes — 62%. The same plane being late once basically guarantees trouble for its next departure. The takeaway: it's not the airline, it's not even the weather — it's the aircraft rotation. The single strongest predictor we found, by a wide margin."

*(124 words)*

---

## 8 · Temporal Patterns · 0:25

> "Two clear temporal patterns. As the day progresses, delay rates climb from about 10% at 5 AM to nearly 30% at 8 PM — the same cascading effect aggregated across the system. On the right: counterintuitively, summer is worse than winter. Convective storms in June through August are short, intense, and harder to plan around than scheduled snow."

*(60 words)*

---

## 9 · Weather · 0:25

> "Weather matters too. Wind: 18% in calm conditions, 34% in strong winds. Precipitation: light rain barely moves the needle, but heavy rain over 10 mm per hour pushes delay rate to 48% — more than double baseline. Both monotonic. But weather still ranks behind cascading delays — bad weather days affect every flight, so the relative signal is smaller."

*(60 words)*

---

## 10 · Airline Reliability · 0:20

> "Two views of airlines. Left: ranked by delay rate. Frontier, Spirit, Allegiant at the top — budget carriers. Delta, United, American at the bottom — legacy. A 5.4-point spread. Right: the actual delay-minute distribution per airline — some have heavier right tails. Tail-risk signal binary classification under-uses."

*(50 words)*

---

## 11 · Hypothesis Tests · 0:35

> "We backed up the EDA with four formal tests, all simulation-based. Test 1: budget vs legacy — permutation, +5.4 pp, p less than one in ten thousand. Test 2: summer vs winter — bootstrap CI, −5.8 pp, doesn't include zero. Test 3: hub vs non-hub — +1.9 pp, smaller but significant. Test 4: weather independence — Monte Carlo chi-squared. All four reject the null."

*(74 words)*

---

## 12 · Null Distributions · 0:20

> "The visual proof. Each gray histogram is the simulated null under no effect. The red line is what we observed. In every panel, the red line is far outside the gray support — that's why all four p-values are essentially zero. Not marginal results."

*(48 words)*

---

## 13 · Modeling Approach · 0:30

> "Now modeling. Binary classification — delayed at least 15 minutes. Most important design choice: temporal split, not random. Train January–October on 5.6 million flights, test November–December on 1.13 million. Random splitting would let rolling features peek at the future. 23 features expanded to 74 columns after one-hot. We benchmarked logistic regression through LightGBM, with randomized hyperparameter search."

*(63 words)*

---

## 14 · ROC Ladder · 0:25

> "The model ladder. Naive baseline at 0.5 AUC — useless. SGD logistic gives the first real signal at 0.757. Random forest jumps to 0.806. XGBoost and LightGBM cluster at 0.81 to 0.82. Notice the four GBDT variants are within 0.005 of each other — we hit a plateau where additional complexity gives diminishing returns."

*(58 words)*

---

## 15 · SMOTE vs Weighted · 0:20

> "Two ways to handle 80:20 imbalance — re-weight the loss with `scale_pos_weight`, or oversample with SMOTE. SMOTE pushed precision up but recall collapsed. Class weighting catches more delays at acceptable precision — F1 4 points higher. SMOTE's synthetic minority points can't capture operational context."

*(48 words)*

---

## 16 · Hyperparameter Tuning · 0:20

> "RandomizedSearchCV — 30 random draws from a 7-dimensional space, scored by ROC-AUC under 3-fold CV. Best config: 400 trees, depth 6, learning rate 0.05. The interesting result is robustness — top 10 configurations sit within 0.002 AUC of each other. We're on a plateau, not a sharp peak."

*(55 words)*

---

## 17 · Threshold Tuning · 0:20

> "Final lever before evaluation: the classification threshold. Default is 0.5. Sweeping the precision-recall curve and picking the F1-maximizer gives 0.573 — slightly above 0.5. F1 climbs from 0.580 to 0.586."

*(36 words)*

---

## 18 · Model Performance ⭐ · 0:50

> "Final results on the 1.13-million-row November–December test set. Tuned XGBoost: AUC 0.817, F1 0.586, threshold 0.573. ROC overlay on the left — green tuned XGBoost on top, the operating-point dot catching about half of all actual delays at 66% precision. The confusion matrix on the right: of 202,000 actual delays, the model catches 52.5%. Of 160,000 alerts, 66.3% are real. Class weights beat SMOTE by 4 F1 points at lower training cost."

*(91 words)*

---

## 19 · Feature Importance · 0:25

> "What the model actually weighs. Cascading-delay — previous-leg arrival delay — at the top by a wide margin, roughly 3× the second-ranked feature on its own. Time-of-day second tier. Weather mid-tier — important but secondary. Airline identity as one-hot dummies in the top 15. The model rediscovered the same hierarchy we saw in EDA."

*(60 words)*

---

## 20 · Regression Detour · 0:25

> "Quick detour — we also tried predicting actual delay minutes. Four models. LightGBM wins — RMSE 32, MAE 14, R-squared 0.27. But typical error is ±14 minutes — same order as the 15-minute threshold itself. Plus residuals are heteroskedastic. So classification stayed our primary deliverable."

*(50 words)*

---

## 21 · Insurance ROI ⭐ · 0:50

> "Concrete dollar value. Delay insurance is priced at the actuarial average — about 18% — so a fair premium is 18% of payout. Buy on every flight: you essentially break even. But our model's precision is 66% — when we flag a flight, it's actually delayed two-thirds of the time, far above the 18% base rate that fair pricing assumes. So if you only insure flagged flights, your realized claim rate is 65.9% against an 18% premium — a 266% ROI, or 3.7× the expected return per dollar of premium. Illustrative, but the broader point: AUC 0.82 is information with real dollar value."

*(108 words)*

---

## 22 · Challenges & Future · 0:30

> "Honest reflections. Memory engineering with parquet plus typed dtypes cut working set 60%. SGD-Logit replaced sklearn saga which timed out at 30 minutes. Class weights beat SMOTE. 500k subsample matches full data within 0.002 AUC. Future: cross-year 2024-to-2025 validation, forecast weather, graph aircraft rotation, per-airport mixture-of-experts, real-time streaming."

*(56 words)*

---

## 23 · Thanks · 0:10

> "That's our project. Thanks — happy to take questions."

*(10 words)*

---

## 📝 Notes for Speakers

- **Pause for emphasis** at ⭐ slides (7, 18, 21) — these are the visual hooks; let the chart breathe before speaking.
- **Numbers to nail**: $30B (slide 2) · 6.8M rows (slide 4) · 80/20 imbalance (slide 5) · 23 features → 74 cols (slide 6) · 62% / 10% cascading (slide 7) · AUC 0.817 / F1 0.586 (slide 18) · 3.7× ROI / 266% / 65.9% (slide 21).
- **Don't read the bullets**. Slides are reference; the script is your voice over them.
- **Transition cues**: §03 Statistical Validation (slides 11–12) closes EDA; §04 Modeling (slides 13–19) is the core; §05 Implications (slide 21) is the payoff.

---

## Adjustments Log
*(Track changes here when revising)*

- 2026-04-27 — v1 draft, ~9:15 total. Replaces prior 14-slide / 14-min script.
