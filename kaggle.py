import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
df = pd.read_csv("messy_data.csv")
df.columns = (
    df.columns.str.strip()
    .str.lower()
    .str.replace(" ", "_")
)

df = df.drop_duplicates()
print(df.isnull().sum())
for col in df.select_dtypes(include="number").columns:
    df[col] = df[col].fillna(df[col].median())
df.to_csv("cleaned_data.csv", index=False)

print("Clean")
print(df.head())
numeric_col = df.select_dtypes(include="number").columns[0]
plt.figure(figsize=(8, 5))
sns.histplot(df[numeric_col].dropna(), kde=True)
plt.title(f"Distribution of {numeric_col}")
plt.tight_layout()
plt.show()
numeric_df = df.select_dtypes(include="number")
plt.figure(figsize=(8, 5))
sns.heatmap(
    numeric_df.corr(),
    annot=True,
    cmap="coolwarm",
    fmt=".2f"
)
plt.title("Correlation Between Numeric Features")
plt.tight_layout()
plt.show()