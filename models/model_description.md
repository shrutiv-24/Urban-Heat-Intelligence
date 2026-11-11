# Model Description

## Objective

Predict the Land Surface Temperature (LST, in °C) of each 30 m pixel in Delhi from its vegetation index (NDVI), and group the predicted temperatures into heat categories.

## Data

- **Source file:** `data/processed/urban_heat_data.csv`
- **Rows:** 1,673,718 valid pixels (a random sample of 300,000 pixels is used for training)
- **Feature:** `ndvi`
- **Target:** `lst_c`

The `uhi` column is stored in the dataset but is **not used as a feature**. UHI is LST minus a constant (the mean LST of Delhi), so using it would give the model the answer directly and produce a meaningless R² of 1.0.

## Training Setup

- **Split:** 80% training data, 20% test data, `random_state=42`
- **Script:** `models/train_model.py`

## Models

### Random Forest Regressor

| Setting | Value |
|---|---|
| n_estimators | 100 |
| min_samples_leaf | 20 |
| random_state | 42 |
| n_jobs | -1 |

Saved as `models/Random_Forest.joblib`. This model is used for the final predictions.

### Linear Regression

Default scikit-learn settings. Saved as `models/Linear_Regression.joblib` and used as a simple baseline.

## Performance (test data)

| Model | MAE (°C) | R² |
|---|---|---|
| Random Forest | 1.733 | 0.324 |
| Linear Regression | 1.759 | 0.297 |

The Random Forest predicts LST with an average error of about 1.7 °C and explains about 32% of the variation. This is consistent with the NDVI and LST correlation of −0.54 (0.54² ≈ 0.29).

## Heat Categories

Predicted LST from the Random Forest is grouped by `urban_heat_intelligence.py`:

| Category | Predicted LST |
|---|---|
| Low | below 40 °C |
| Moderate | 40 to 42 °C |
| High | 42 to 44 °C |
| Extreme | above 44 °C |

Predicted values range from 33.14 °C to 45.38 °C, with a mean of 41.62 °C.

## Limitations

- NDVI is the only feature, so the model explains only part of the temperature variation. Built-up surfaces, building density and materials also affect LST.
- Predictions are smoother than the observed LST (29.0 to 53.7 °C), so the highest temperatures are under-represented.
- The model was trained on a single April to June 2023 composite for Delhi and should not be applied to other cities or seasons without retraining.

## Possible Improvements

Add predictors such as NDBI (built-up index), elevation and land use, and train on several years of imagery.