# Synthetic Data Assumptions – QuickBite Analytics
## Team: Data Knights | CODEGNAN DA-07

> **DISCLAIMER:** All data in this project is explicitly SYNTHETIC.
> It is generated for demonstration and educational purposes only.
> It does NOT represent actual QuickBite, restaurant, customer, or rider records.

---

## 1. Business Context Assumptions

| Assumption | Value | Rationale |
|---|---|---|
| Operating cities | Hyderabad, Visakhapatnam, Vijayawada | As specified in problem statement |
| City size weighting | 55% / 25% / 20% | Proportional to approximate population sizes |
| Analysis period | January – December 2024 | Full calendar year for trend analysis |
| Customer signup window | January 2023 – December 2024 | 2-year window creates mix of new/established customers |
| Total partners | ~4,000 restaurants | As specified in problem statement |

---

## 2. Order Volume & Distribution

| Assumption | Value | Rationale |
|---|---|---|
| Total orders | ~100,000 | As specified in problem statement |
| Peak lunch hours | 12:00–14:00 | Standard Indian food delivery patterns |
| Peak dinner hours | 19:00–22:00 | Standard Indian food delivery patterns |
| Weekend boost | Not separately modeled | Simplified for hackathon scope |
| Order value distribution | Log-normal (μ=5.8, σ=0.5) | Captures long tail of expensive orders; range INR 80–3,000 |
| Discount rate | 45% of orders have discounts | Reflects common promotional pricing in Indian food delivery |
| Discount range | 5–30% of order value | Typical coupon/offer ranges |

---

## 3. Customer Behavior

| Assumption | Value | Rationale |
|---|---|---|
| Order frequency distribution | Negative binomial (r=1, p=0.35) | Creates realistic skew: many one-timers, few heavy users |
| Repeat customer threshold | ≥ 2 orders | Standard industry definition |
| Customer city match | Customer orders from restaurants in their city | Simplified — no inter-city ordering |
| No personal data stored | Name, phone, email, address excluded | Privacy best practice |

---

## 4. Restaurant Performance

| Assumption | Value | Rationale |
|---|---|---|
| Restaurant rating distribution | Normal (μ=3.9, σ=0.5), clipped 1–5 | Most restaurants are slightly above average |
| Preparation time | Cuisine-dependent normal distribution | Biryani takes longer than burgers |
| Restaurant location | All 3 cities | Proportional to city weights |

**Preparation Time by Cuisine (minutes):**

| Cuisine | Mean | Std Dev |
|---|---|---|
| Biryani | 25 | 8 |
| Seafood | 25 | 7 |
| Continental | 22 | 6 |
| North Indian | 20 | 6 |
| Pizza | 20 | 6 |
| South Indian | 15 | 5 |
| Healthy | 15 | 4 |
| Chinese | 18 | 5 |
| Thali | 20 | 5 |
| Rolls & Wraps | 12 | 3 |
| Burger | 12 | 4 |
| Desserts | 10 | 4 |
| Fast Food | 10 | 3 |

---

## 5. Delivery Operations

| Assumption | Value | Rationale |
|---|---|---|
| Delivery distance | Log-normal (μ=1.8, σ=0.5), clipped 0.5–22 km | Urban delivery; most within 5–10 km |
| Rider speed | Uniform 14–20 km/h | City traffic conditions in Indian metros |
| On-time threshold | Delay ≤ 5 minutes | Industry-standard tolerance |
| Delay during peak hours | Higher probability of delay 12–14h and 19–22h | Traffic congestion |
| On-time delivery rate | ~65–70% | Realistic for Indian food delivery market |
| Cancelled orders get no delivery | TRUE | Enforced in data generation |

**Delay Model:**

| Probability Range | Delay Type | Delay Range |
|---|---|---|
| 0–60% | On time or early | -5 to +5 minutes |
| 60–85% | Mild delay | 5–25 minutes |
| 85–100% | Severe delay | 25–70 minutes |

During peak hours, the threshold for delay is reduced (more orders delayed).

---

## 6. Order Status Distribution

| Status | Approximate % | Notes |
|---|---|---|
| Completed | ~86–88% | Normal successful orders |
| Cancelled | ~8–14% (peaks during 19–22h) | Higher at dinner peak |
| Refunded | ~2% | System/quality refunds |
| Partially Delivered | ~1% | Rare incomplete deliveries |

---

## 7. Customer Feedback

| Assumption | Value | Rationale |
|---|---|---|
| Feedback rate | ~80% of completed orders | High engagement for demonstration |
| Rating model | Restaurant rating + noise − delay penalty | Reflects real-world correlation |
| Delay penalty | delay_minutes / 30 (max −2 points) | Proportional to severity |
| Complaint threshold | Rating ≤ 3 OR delay > 20 minutes | Industry-typical complaint triggers |
| Refund probability | 1-star: 50–100% of order value; 2-star: 0–30% | Proportional to dissatisfaction |

---

## 8. Dirty Data Assumptions

The dirty dataset copies introduce the following issues for cleaning demonstration:

| Issue Type | Frequency | Affected Tables |
|---|---|---|
| Missing values | ~3% of key numeric/string columns | All tables |
| Duplicate rows | ~1% extra rows | All tables |
| Negative values in numeric fields | ~0.5% | orders, deliveries |
| Mixed date formats | ~2% of timestamps | orders |
| Inconsistent text case (UPPERCASE) | ~3% of first string column | All tables |
| Out-of-range ratings | ~0.5% | feedback |

---

## 9. Intentional Design Choices

1. **Not every hypothesis is forced to be true.** Ratings and delays are correlated but noisy. Some highly-rated restaurants still have occasional delays.

2. **City proportions reflect reality.** Hyderabad dominates as a larger metro; Vizag and Vijayawada are smaller markets.

3. **Outliers are preserved in raw data.** A small fraction of very high order values and very long delivery times represent legitimate edge cases (large catering orders, traffic incidents).

4. **Referential integrity is maintained.** Every order references a valid customer, restaurant, and rider. Every delivery references a valid order.

5. **Temporal consistency.** Pickup time is always after order time. Delivery time is always after pickup time. No future timestamps.

---

## 10. Random Seed

All random number generation uses seed **42** for full reproducibility.
Re-running `generate_dataset.py` will produce identical datasets.
