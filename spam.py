import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import (
    accuracy_score,
    confusion_matrix,
    classification_report,
    ConfusionMatrixDisplay
)
from sklearn.pipeline import Pipeline
df = pd.read_csv(
    "SMSSpamCollection",
    sep="\t",
    header=None,
    names=["label", "message"],
    encoding="utf-8"
)
print("Dataset shape:", df.shape)
print(df.head())
print("\nClass counts:\n", df["label"].value_counts())
X = df["message"]
y = df["label"]
X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.2,
    random_state=42,
    stratify=y
)
model = Pipeline([
    ("tfidf", TfidfVectorizer()),
    ("classifier", MultinomialNB())
])
model.fit(X_train, y_train)
predictions = model.predict(X_test)
accuracy = accuracy_score(y_test, predictions)
print(f"\nAccuracy: {accuracy * 100:.2f}%")
print("\nClassification Report:")
print(classification_report(y_test, predictions))

labels = ["ham", "spam"]
cm = confusion_matrix(y_test, predictions, labels=labels)

print("\nConfusion Matrix (rows=actual, columns=predicted):")
print(pd.DataFrame(
    cm,
    index=["Actual ham", "Actual spam"],
    columns=["Predicted ham", "Predicted spam"]
))
ConfusionMatrixDisplay(
    confusion_matrix=cm,
    display_labels=labels
).plot()
plt.title("SMS Spam Detection Confusion Matrix")
plt.tight_layout()
plt.show()
message = input("\nEnter an SMS to classify: ")
prediction = model.predict([message])[0]
print("Prediction:", prediction.upper())
