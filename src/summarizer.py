import pandas as pd
from collections import defaultdict

def summarize_groups(pages):
    """Summarize grouped pages into cluster-level overview."""
    groups = defaultdict(list)
    for p in pages:
        groups[p["cluster_id"]].append(p)

    summary_data = []
    for group_id, records in groups.items():
        # Determine dominant category
        category_counts = {}
        for r in records:
            category_counts[r["category"]] = category_counts.get(r["category"], 0) + 1
        dominant_category = max(category_counts, key=category_counts.get)

        # First non-empty DOS (you can also assume all have same DOS)
        dos = next((r["dos"] for r in records if r["dos"]), "Not found")

        # First non-empty facility
        facility = next((r["facility"] for r in records if r["facility"]), "Not found")

        # FIRST non-empty provider (using improved extraction)
        provider = next((r["provider"] for r in records if r["provider"]), "Not found")

        summary_data.append({
            "Group ID": group_id,
            "Category": dominant_category,
            "Page Count": len(records),
            "DOS": dos,
            "Facility": facility,
            "Provider": provider
        })

    return pd.DataFrame(summary_data).sort_values("Group ID")
