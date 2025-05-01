# src/output_writer.py
import pandas as pd

def save_to_csv(pages, output_path="grouped_pages.csv"):
    """
    Saves grouped pages with full metadata to CSV.
    Columns: page_num, cluster_id, category, dos, provider, facility, header
    """
    records = []
    for p in pages:
        records.append({
            "page_num": p["page_num"],
            "cluster_id": p["cluster_id"],
            "category": p["category"],
            "dos": p["dos"],
            "provider": p["provider"],
            "facility": p["facility"],
            "header": p["header"]
        })
    df = pd.DataFrame(records)
    df.to_csv(output_path, index=False)
    print(f"Saved grouped records to {output_path}")
