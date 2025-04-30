from .pdf_extractor import extract_pages
from .text_cleaner import clean_text
from .clusterer import get_embeddings, cluster_pages

import re
from datetime import datetime

def extract_page_metadata(page):
    text = page.get("text", "") or ""
    page_num = page.get("page_num", 0)

    # Category
    if "lab" in text.lower():
        category = "Lab"
    elif "progress note" in text.lower() or "clinical note" in text.lower():
        category = "Clinical Note"
    elif "urology" in text.lower():
        category = "Urology Note"
    else:
        category = "Other"

    # Providers
    providers = "; ".join(re.findall(r'Electronically signed by[: ]+([^\n(]+)', text))

    # DOS
    date_matches = re.findall(r'\b\d{1,2}/\d{1,2}/(?:19|20)?\d{2}\b', text)
    dos = max(date_matches, default="")  # Latest date found, or blank

    # Facility
    facility_match = re.search(r'\bABC FACILITY\b', text.upper())
    facility = "ABC Facility" if facility_match else ""

    return {
        "pagenumber": page_num,
        "category": category,
        "providers": providers,
        "dos": dos,
        "facility": facility
    }

def group_pages(pdf_path):
    pages = extract_pages(pdf_path)
    cleaned_texts = [clean_text(page['text']) for page in pages]
    embeddings = get_embeddings(cleaned_texts)
    clusters = cluster_pages(embeddings)

    for page, cluster_id in zip(pages, clusters):
        page['cluster_id'] = cluster_id
        page.update(extract_page_metadata(page))

    return pages

if __name__ == "__main__":
    grouped = group_pages("data/Sample Document.pdf")
    for page in grouped:
        print(f"Page {page['pagenumber']} | Category: {page['category']} | DOS: {page['dos']} | Providers: {page['providers']}")
