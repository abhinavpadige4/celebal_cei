import pandas as pd

df = pd.read_csv("expenses.csv")
df["date"] = pd.to_datetime(df["date"])

month = input("Enter month (YYYY-MM): ")

total = df.loc[
    df["date"].dt.strftime("%Y-%m") == month,
    "amount"
].sum()

print(f"Total expenses: ₹{total:.2f}")