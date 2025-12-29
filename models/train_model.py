import pandas as pd
from sklearn.ensemble import RandomForestRegressor
import joblib

# Load historical data
df = pd.read_csv("data/battery_data.csv")

X = df[["soc", "temperature", "charge_cycles"]]
y = df["health_score"]

model = RandomForestRegressor(
    n_estimators=100,
    max_depth=6,
    random_state=42
)

model.fit(X, y)

joblib.dump(model, "models/battery_model.pkl")
print("Model trained and saved.")
