import pandas as pd
from collections import defaultdict

def summarize_groups(pages):
    """Summarize grouped pages into cluster-level overview."""
    groups = defaultdict(list)
    for p in pages:
        groups[p["cluster_id"]].append(p)

    summary_data = []
    for group_id, records in groups.items():
        category_counts = {}
        for r in records:
            cat = r["category"]
            category_counts[cat] = category_counts.get(cat, 0) + 1

        dominant_category = max(category_counts, key=category_counts.get)
        summary_data.append({
            "Group ID": group_id,
            "Category": dominant_category,
            "Page Count": len(records),
            "DOS": records[0]["dos"] if records else "",
            "Facility": records[0]["facility"] if records else "",
            "Provider": records[0]["provider"] if records else ""
        })

    return pd.DataFrame(summary_data).sort_values("Group ID")
