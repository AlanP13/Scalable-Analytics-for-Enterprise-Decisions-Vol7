# Results

This file records the quantitative results referenced in the monograph. The
values are produced by the evaluation scripts in `code/`. The vehicle-price
figures below are the reported results from the study; the forecasting exact
figures regenerate when the script is run (the source study reported them
directionally, shown below).

## Vehicle-price prediction (MSDS-532, Extremely Randomized Trees)

Evaluation: held-out test split. Predictor influence by permutation importance.
Script: `code/msds532-vehicle-price/`.

| Metric | Training | Test |
|---|---|---|
| R-squared | 0.9991 | 0.9075 |
| RMSE | 300.17 | 2881.55 |

Top predictors by permutation importance (descending):

1. Registration year (by far the strongest predictor)
2. Vehicle model
3. Gearbox type

Note: mileage contributed less than expected relative to registration year.

## Retail forecasting (ITS-836)

Target: weekly series from the Walmart dataset. Features: holiday window,
lags, rolling windows, discount intensity, CPI, unemployment. Split: chronological
80 percent train / 20 percent test. Models compared: Naive Lag-1 (baseline),
SARIMA, Random Forest, XGBoost. Metrics: RMSE, MAE, R-squared.
Script: `code/its836-holiday-forecasting/`.

Directional result reported in the source study:

| Model | RMSE | MAE | R-squared |
|---|---|---|---|
| Naive Lag-1 (baseline) | Higher | Higher | Lower |
| Random Forest | Lower | Lower | Higher |

Exact per-model figures (fill from the script output before sharing widely):

| Model | RMSE | MAE | R-squared |
|---|---|---|---|
| Naive Lag-1 | TBD | TBD | TBD |
| SARIMA | TBD | TBD | TBD |
| Random Forest | TBD | TBD | TBD |
| XGBoost | TBD | TBD | TBD |

Top predictors: a lagged value was the strongest, followed by macroeconomic
(CPI, unemployment) and holiday features.

Notes:
- Record library versions and the random seed so the figures regenerate.
- Record the exact train/test split definition (selected store-department series).
