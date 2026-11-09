import os
import joblib
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

DATA_PATH = "data/processed/urban_heat_data.csv"
MODEL_PATH = "models/Random_Forest.joblib"
OUTPUT_DIR = "results"

os.makedirs(OUTPUT_DIR, exist_ok=True)

data = pd.read_csv(DATA_PATH)
model = joblib.load(MODEL_PATH)

features = ["ndvi", "uhi"]
X = data[features]

predictions = model.predict(X)

data["predicted_lst"] = predictions

data["heat_category"] = pd.cut(
    predictions,
    bins=[-np.inf, 25, 35, 45, np.inf],
    labels=["Low", "Moderate", "High", "Extreme"]
)

data.to_csv(
    os.path.join(OUTPUT_DIR, "urban_heat_predictions.csv"),
    index=False
)

plt.figure(figsize=(10, 6))
sns.histplot(predictions, bins=30, kde=True)
plt.title("Predicted Urban Heat Distribution")
plt.xlabel("Predicted LST")
plt.ylabel("Pixel Count")
plt.tight_layout()
plt.savefig(
    os.path.join(OUTPUT_DIR, "temperature_distribution.png")
)
plt.close()

plt.figure(figsize=(10, 6))
sns.scatterplot(
    data=data,
    x="ndvi",
    y="predicted_lst",
    hue="heat_category"
)
plt.title("NDVI vs Predicted Urban Heat")
plt.tight_layout()
plt.savefig(
    os.path.join(OUTPUT_DIR, "ndvi_heat_analysis.png")
)
plt.close()

plt.figure(figsize=(8, 6))
sns.countplot(
    data=data,
    x="heat_category",
    hue="heat_category",
    order=["Low", "Moderate", "High", "Extreme"],
    legend=False
)
plt.title("Urban Heat Category Distribution")
plt.tight_layout()
plt.savefig(
    os.path.join(OUTPUT_DIR, "heat_categories.png")
)
plt.close()

print("\nURBAN HEAT ANALYSIS COMPLETED")

print("\nHeat Category Counts:")
print(data["heat_category"].value_counts())

print("\nAverage Prediction:")
print(round(np.mean(predictions), 2))

print("\nMaximum Prediction:")
print(round(np.max(predictions), 2))

print("\nMinimum Prediction:")
print(round(np.min(predictions), 2))

print("\nFiles saved in results/")