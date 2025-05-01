import re
import pdfplumber

import re
import pdfplumber

def extract_metadata(text, header):
    # Look in the full text first
    provider_match = re.search(r'(Dr\.?\s+[A-Z][a-z]+(?:\s+[A-Z][a-z]+)?)', text)
    if not provider_match:
        # Fallback to header
        provider_match = re.search(r'(Dr\.?\s+[A-Z][a-z]+(?:\s+[A-Z][a-z]+)?)', header)
    # (DOS and facility extraction unchanged)
    dos_match = re.search(r'(\d{1,2}/\d{1,2}/\d{2,4})', text + header)
    facility_match = re.search(r'(Hospital|Clinic|Medical Center|Health Center)', text + header, re.IGNORECASE)

    return {
        "dos": dos_match.group(1) if dos_match else "",
        "provider": provider_match.group(0) if provider_match else "",
        "facility": facility_match.group(1).title() if facility_match else ""
    }

def extract_pages(pdf_path):
    pages_data = []
    with pdfplumber.open(pdf_path) as pdf:
        for page_num, page in enumerate(pdf.pages, start=1):
            text = page.extract_text() or ""
            lines = text.split('\n')
            header = lines[0] if lines else ""
            footer = lines[-1] if lines else ""

            metadata = extract_metadata(text, header)
            category = detect_category(text)

            pages_data.append({
                "page_num": page_num,
                "text": text,
                "header": header,
                "footer": footer,
                **metadata,
                "category": category
            })
    return pages_data

def extract_pages(pdf_path):
    pages_data = []

    with pdfplumber.open(pdf_path) as pdf:
        for page_num, page in enumerate(pdf.pages, start=1):
            text = page.extract_text() or ""
            lines = text.split('\n')
            header = lines[0] if lines else ""
            footer = lines[-1] if lines else ""

            metadata = extract_metadata(text)

            pages_data.append({
                "page_num": page_num,
                "text": text,
                "header": header,
                "footer": footer,
                **metadata  # adds dos, provider, facility
            })

    return pages_data
import re
import pdfplumber

def extract_metadata(text):
    dos_match = re.search(r'(\d{1,2}/\d{1,2}/\d{2,4})', text)
    provider_match = re.search(r'(Dr\.?\s+[A-Z][a-z]+\s+[A-Z][a-z]+)', text)
    facility_match = re.search(r'(Hospital|Clinic|Medical Center|Health Center)', text, re.IGNORECASE)

    return {
        "dos": dos_match.group(1) if dos_match else "",
        "provider": provider_match.group(1) if provider_match else "",
        "facility": facility_match.group(1).title() if facility_match else ""
    }

def detect_category(text):
    categories = {
        "Lab Report": ["hemoglobin", "cbc", "blood test", "lab result", "specimen", "reference range"],
        "Progress Note": ["progress note", "consultation", "clinical note", "visit", "follow-up", "assessment"],
        "Discharge Summary": ["discharge", "hospital course", "admission", "summary of care"],
        "Medication List": ["medications", "prescription", "drug", "pharmacy", "dose", "medication"]
    }

    for cat, keywords in categories.items():
        if any(kw.lower() in text.lower() for kw in keywords):
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

            pages_data.append(page_info)

    return pages_data
