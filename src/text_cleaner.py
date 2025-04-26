import re

def clean_text(text):
    if not text:
        return ""

    # Convert to lowercase
    text = text.lower()

    # Remove non-ASCII characters
    text = text.encode("ascii", errors="ignore").decode()

    # Remove multiple spaces and newlines
    text = re.sub(r'\s+', ' ', text)

    # Optional: Remove dates or symbols if needed
    # text = re.sub(r'\d{1,2}/\d{1,2}/\d{2,4}', '', text)  # Remove dates like 01/01/2022

    return text.strip()

# Sample usage for testing
if __name__ == "__main__":
    raw = """
        LAB REPORT - PATIENT NAME: John Doe ©
        DATE: 01/02/2024
        Test Result: Normal
    """
    cleaned = clean_text(raw)
    print("Cleaned Text:", cleaned)
