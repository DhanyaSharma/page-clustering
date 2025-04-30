import pdfplumber

def extract_pages(pdf_path):
    """
    Extracts text and page number from each PDF page.
    """
    pages_data = []

    with pdfplumber.open(pdf_path) as pdf:
        for page_num, page in enumerate(pdf.pages, start=1):
            text = page.extract_text()
            page_info = {
                "page_num": page_num,
                "text": text or ""
            }
            pages_data.append(page_info)

    return pages_data

if __name__ == "__main__":
    pdf_path = "data/SampleDocument.pdf"
    pages = extract_pages(pdf_path)
    for page in pages:
        print(f"Page {page['page_num']} | Text starts with: {page['text'][:60]}")
