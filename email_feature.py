import re


def extract_email_features(email_content):
    features = []
    # Example: Check if the email has suspicious keywords
    phishing_keywords = ["urgent", "verify", "account", "password", "login"]
    suspicious_count = sum(email_content.lower().count(word) for word in phishing_keywords)
    features.append(suspicious_count)

    # Example: Check the length of the email content
    features.append(len(email_content))

    # Add more feature extraction logic here
    return features
