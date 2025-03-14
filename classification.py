import joblib
import pandas as pd

# Load the trained model and vectorizer
model = joblib.load("tax_model.pkl")
vectorizer = joblib.load("vectorizer.pkl")

def classify_transaction(description, amount):
    """
    Uses ML model to predict if a transaction is 'Taxable' or 'Non-Taxable'.
    """
    desc_vectorized = vectorizer.transform([description])
    input_data = pd.concat([pd.DataFrame(desc_vectorized.toarray()), pd.DataFrame([[amount]])], axis=1)

    prediction = model.predict(input_data)[0]
    return "Taxable" if prediction == 1 else "Non-Taxable"

# Example Usage
if __name__ == "__main__":
    print(classify_transaction("Freelance Work Payment", 1500))  # Output: Taxable
