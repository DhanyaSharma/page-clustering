import re

def clean_text(text):
    if not text:
        return ""

    text = text.lower()
    text = text.encode("ascii", errors="ignore").decode()
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

if __name__ == "__main__":
    raw = """
        LAB REPORT - PATIENT NAME: Remo Remo ©
        DATE: 01/02/2024
        Test Result: Normal
    """
    cleaned = clean_text(raw)
    print("Cleaned Text:", cleaned)
