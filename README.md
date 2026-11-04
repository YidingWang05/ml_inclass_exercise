# ELEC70143 Machine Learning In-Class Exercise

**2025/2027**

## Air Pollution Monitoring System

Design a compact, low-cost air-quality monitor that estimates carbon monoxide (CO) concentration from electrochemical and meteorological sensors. Reference-grade sensors are expensive, while lower-cost sensors provide noisier signals.

1. Build and compare regression models that predict CO concentration.
2. Quantify the trade-off between prediction accuracy and hardware cost.
3. Recommend a cost-effective sensor configuration.

## Data

Use `q1.csv`. Each row represents a snapshot of ambient conditions and sensor responses collected in an Italian city in 2004–2005. The regression target is **`CO(GT)`**, the reference CO concentration in mg/m³. The remaining variables are predictors.

| Variable | Description | Typical range | Cost (£) |
| --- | --- | ---: | ---: |
| `PT08.S1(CO)` | Tin oxide sensor response (ppm) | 300–1800 | 1,000 |
| `PT08.S2(NMHC)` | Non-methane hydrocarbon sensor | 400–2000 | 800 |
| `PT08.S3(NOx)` | Nitrogen oxide sensor | 400–2000 | 700 |
| `PT08.S4(NO2)` | Nitrogen dioxide sensor | 400–2000 | 700 |
| `PT08.S5(O3)` | Ozone sensor | 400–2000 | 900 |
| `T` | Temperature (°C) | −10–40 | 150 |
| `RH` | Relative humidity (%) | 0–100 | 150 |
| `AH` | Absolute humidity | 0–50 | 200 |
| `NOx(GT)` | Reference NOₓ concentration | 0–600 | 1,800 |
| `NO2(GT)` | Reference NO₂ concentration | 0–250 | 1,800 |
| `C6H6(GT)` | Benzene concentration (µg/m³) | 0–15 | 2,500 |
| `CO(GT)` | Ground-truth CO concentration (mg/m³) | 0–10 | — |

Data reference — De Vito, S., Massera, E., Piga, M., Martinotto, L., & Di Francia, G. (2008). *On field calibration of an electronic nose for benzene estimation in an urban pollution monitoring scenario.*

## A. Handle missing data

Import the data into Python and report the percentage of missing entries (`NaN`) for each feature. Choose, justify, and implement a strategy such as mean or median imputation, k-nearest-neighbour imputation, or model-based imputation.

## B. Explore distributions and correlations

Use a correlation plot or pairs plot to examine the main features and the target. Discuss strong correlations and potential multicollinearity.

## C. Fit ordinary least squares

Randomly split the data into 80% training and 20% test sets. Fit an OLS model with all predictors using a tool such as `statsmodels.OLS`. Provide the model summary, identify statistically significant variables, and discuss what you can conclude. Explain why some coefficients may be unusually large or have large p-values.

## D. Fit ridge and lasso

Use cross-validation to tune the regularisation parameter for ridge and lasso. Fit on scaled features and plot the coefficient paths with the regularisation parameter on a logarithmic axis. Discuss the effects on multicollinearity and interpretability.

## E. Compare model performance

Report training and test R², MAE, and RMSE for OLS, ridge, and lasso. Compare their predictive performance and interpretability.

## F. Choose sensors within budget

A portable monitor has a maximum hardware budget of **£4,000**. Use the sensor prices above and fit a lasso path over a grid of regularisation parameters, for example from 10⁻⁶ to 1. For each candidate, record:

- The features with nonzero coefficients.
- The total purchase cost of those features.
- The five-fold cross-validated RMSE on the training data.

Order the candidates by cost and plot cost against CV RMSE to visualise the trade-off. Choose a low-cost design (at most **£2,500**) and a high-performance design (at most **£4,000**). Report the test-set RMSE of each design.

## G. Choose an alert threshold

An actual exceedance occurs when measured CO is greater than **5 mg/m³**. Issue an alert when predicted CO is greater than a candidate threshold `t`.

| Error | Cost |
| --- | ---: |
| False positive (unnecessary alert) | £2,000 |
| False negative (missed exceedance) | £10,000 |

Sweep a range of candidate thresholds. Use cross-validation or a separate validation set to estimate the expected cost for each threshold. The average cost per reading is `(2000 × false positives + 10000 × false negatives) / number of readings`. Use these results to select a threshold.

## H. Compare the monitor designs

Compare the expected alert costs of the low-cost and high-performance monitors. Discuss the difference and whether the expected savings justify the added sensor cost.
