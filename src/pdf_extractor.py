import re
import pdfplumber

def extract_metadata(text):
    # Debugging output to check the extracted text
    print("Extracted Text:\n", text[:500])  # Print the first 500 characters of the text

    # Update DOS extraction (DOB is commonly used as date of service in the text)
    dos_match = re.search(r'DOB:\s*(\d{1,2}/\d{1,2}/\d{2,4})', text)
    dos = dos_match.group(1) if dos_match else "Not found"

    # Update Provider extraction logic (to allow variations like D.O. and extra spaces)
    provider = ""
    m = re.search(r'Electronically signed by:\s*([A-Za-z\s\(\)\.]+(?:\(.+?\))?)', text)
    if m:
        provider = m.group(1).strip()
    else:
        m = re.search(r'Provider Details\s*Provider\s*([A-Za-z\s\(\)\.]+(?:\(.+?\))?)', text)
        if m:
            provider = m.group(1).strip()
        else:
            m = re.search(r'(Dr\.?\s*[A-Za-z]+(?:\s+[A-Za-z]+)?)', text)
            if m:
                provider = m.group(1).strip()

    # Update Facility extraction logic (case-insensitive matching)
    facility_match = re.search(r'(ABC FACILITY|Hospital|Clinic|Medical Center|Health Center)', text, re.IGNORECASE)
    facility = facility_match.group(1).title() if facility_match else "Not found"

    return {"dos": dos, "provider": provider, "facility": facility}
def detect_category(text):
    categories = {
        "Lab Report": ["hemoglobin", "cbc", "blood test", "lab result", "specimen", "reference range"],
        "Progress Note": ["progress note", "consultation", "clinical note", "visit", "follow-up", "assessment"],
        "Discharge Summary": ["discharge", "hospital course", "admission", "summary of care"],
        "Medication List": ["medications", "prescription", "drug", "pharmacy", "dose", "medication"]
    }
    for cat, kws in categories.items():
        if any(kw.lower() in text.lower() for kw in kws):
            return cat
    return "N/A"

def extract_pages(pdf_path):
    pages_data = []
    with pdfplumber.open(pdf_path) as pdf:
        for page_num, page in enumerate(pdf.pages, start=1):
            text = page.extract_text() or ""
            lines = text.split('\n')
            header = lines[0] if lines else ""
            footer = lines[-1] if lines else ""

            metadata = extract_metadata(text)
            category = detect_category(text)

            page_info = {
                "page_num": page_num,
                "text": text,
                "header": header,
                "footer": footer,
                "dos": metadata["dos"],
                "provider": metadata["provider"],
                "facility": metadata["facility"],
                "category": category
            }

            # Debug: uncomment to see extraction
            print(f"[Page {page_num}] Provider: {metadata['provider']} | DOS: {metadata['dos']} | Facility: {metadata['facility']}")

            pages_data.append(page_info)
    return pages_data
def extract_provider(text):
    # Match typical doctor patterns
    pattern = r"\b(?:Dr\.|Doctor|D\.O\.|MD)\s([A-Za-z\s]+)"
    match = re.search(pattern, text)
    if match:
        return match.group(1)  # Return the name after the title
    return "Not found"  # Fallback when no provider is found