import os
import joblib
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, r2_score

DATA_PATH = "data/processed/urban_heat_data.csv"
MODEL_DIR = "models"

os.makedirs(MODEL_DIR, exist_ok=True)

data = pd.read_csv(DATA_PATH)

features = ["ndvi"]
target = "lst_c"

data = data.dropna(subset=features + [target])

data = data.sample(n=min(300000, len(data)), random_state=42)

X = data[features]
y = data[target]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

models = {
    "Random_Forest": RandomForestRegressor(
        n_estimators=100,
        min_samples_leaf=20,
        random_state=42,
        n_jobs=-1
    ),
    "Linear_Regression": LinearRegression()
}

for name, model in models.items():

    model.fit(X_train, y_train)

    predictions = model.predict(X_test)

    mae = mean_absolute_error(y_test, predictions)
    r2 = r2_score(y_test, predictions)

    model_path = os.path.join(
        MODEL_DIR, f"{name}.joblib"
    )

    joblib.dump(model, model_path)

    print("\nModel:", name)
    print("MAE:", round(mae, 3))
    print("R2 Score:", round(r2, 3))
    print("Saved:", model_path)

print("\nALL MODELS TRAINED SUCCESSFULLY!")