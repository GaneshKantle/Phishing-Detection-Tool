import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import pickle

# Load Email Dataset
email_data = pd.read_csv("dataset/email_data.csv")

# Feature Extraction
X_email = email_data.drop(["label"], axis=1)
y_email = email_data["label"]

# Train-Test Split
X_train, X_test, y_train, y_test = train_test_split(X_email, y_email, test_size=0.2, random_state=42)

# Random Forest Classifier
email_model = RandomForestClassifier(n_estimators=100, random_state=42)
email_model.fit(X_train, y_train)

# Save Model
pickle.dump(email_model, open("email_model.pkl", "wb"))

print("Email Phishing Detection Model Trained and Saved Successfully!")
