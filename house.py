import pandas as pd
import matplotlib.pyplot as plt
from sklearn.datasets import fetch_california_housing
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from math import sqrt

housing = fetch_california_housing(as_frame=True)
df = housing.frame

X = df.drop(columns=["MedHouseVal"])
y = df["MedHouseVal"]

print("Dataset shape:", df.shape)
print(df.head())
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)
models = {
    "Linear Regression": LinearRegression(),
    "Random Forest": RandomForestRegressor(
        n_estimators=100, random_state=42, n_jobs=-1
    )
}
results = []

for name, model in models.items():
    model.fit(X_train, y_train)
    predictions = model.predict(X_test)

    results.append({
        "Model": name,
        "MAE": mean_absolute_error(y_test, predictions),
        "RMSE": sqrt(mean_squared_error(y_test, predictions)),
        "R2 Score": r2_score(y_test, predictions)
    })

    print(f"\n{name}")
    print("Sample predictions (in $100,000 units):")
    print(predictions[:5])
results_df = pd.DataFrame(results)
print("\nModel Comparison:")
print(results_df.round(4).to_string(index=False))
results_df.plot(
    x="Model", y=["MAE", "RMSE"],
    kind="bar", figsize=(8, 5)
)
plt.title("Regression Model Error Comparison")
plt.ylabel("Error (lower is better)")
plt.xticks(rotation=0)
plt.tight_layout()
plt.show()
best_name = results_df.loc[results_df["RMSE"].idxmin(), "Model"]
best_model = models[best_name]
sample = X_test.iloc[[0]]
predicted_value = best_model.predict(sample)[0]
print("\nBest model by RMSE:", best_name)
print(f"Predicted median house value: ${predicted_value * 100000:,.0f}")
print(f"Actual median house value: ${y_test.iloc[0] * 100000:,.0f}")
