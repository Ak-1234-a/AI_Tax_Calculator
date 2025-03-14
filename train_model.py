import pandas as pd
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier

# Load dataset
df = pd.read_csv("tax_data.csv")

# Convert labels to numeric (Taxable = 1, Non-Taxable = 0)
df["Tax Classification"] = df["Tax Classification"].map({"Taxable": 1, "Non-Taxable": 0})

# Text vectorization (Convert transaction descriptions to numerical features)
vectorizer = TfidfVectorizer()
X_text = vectorizer.fit_transform(df["Description"])

# Convert sparse matrix to DataFrame with string column names
X_text_df = pd.DataFrame(X_text.toarray(), columns=[str(i) for i in range(X_text.shape[1])])

# Combine text features with amount column
X = pd.concat([X_text_df, df["Amount"].reset_index(drop=True)], axis=1)

# Ensure column names are strings
X.columns = X.columns.astype(str)

# Target variable
y = df["Tax Classification"]

# Split dataset
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train model
model = RandomForestClassifier()
model.fit(X_train, y_train)

# Save the trained model and vectorizer
joblib.dump(model, "tax_model.pkl")
joblib.dump(vectorizer, "vectorizer.pkl")

print("✅ Model training complete and saved!")
