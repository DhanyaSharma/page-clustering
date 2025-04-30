import pandas as pd

def save_to_csv(pages, output_path="grouped_pages.csv"):
    data = [{
        "pagenumber": page.get('pagenumber'),
        "category": page.get('category'),
        "providers": page.get('providers'),
        "dos": page.get('dos'),
        "facility": page.get('facility')
    } for page in pages]

    df = pd.DataFrame(data)
    df.to_csv(output_path, index=False)
    print(f"Grouped pages saved to {output_path}")


if __name__ == "__main__":
    from group_pages import group_pages
    pages = group_pages("data/Sample Document.pdf")
    save_to_csv(pages)
