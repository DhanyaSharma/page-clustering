from collections import defaultdict
from src.text_cleaner import clean_text
from src.pdf_extractor import extract_pages
from src.clusterer import get_embeddings, cluster_pages
from copy import deepcopy

def carry_forward_metadata(pages):
    clusters = defaultdict(list)
    for page in pages:
        clusters[page["cluster_id"]].append(page)

    for group in clusters.values():
        ref = next((p for p in group if p["dos"] or p["provider"] or p["facility"]), {})
        for page in group:
            for field in ["dos", "provider", "facility"]:
                if not page.get(field) and ref.get(field):
                    page[field] = ref[field]
    return pages

def merge_small_groups(pages):
    merged = []
    prev = None
    new_cluster_id = 0

    pages = sorted(pages, key=lambda x: x["page_num"])
    for page in pages:
        if page["category"] == "N/A" and prev and page["dos"] == prev["dos"] and page["facility"] == prev["facility"]:
            page["cluster_id"] = prev["cluster_id"]
        else:
            page["cluster_id"] = new_cluster_id
            new_cluster_id += 1
        prev = page
        merged.append(page)
    return merged

def merge_orphan_na(pages):
    merged = []
    prev = None

    for i, page in enumerate(sorted(pages, key=lambda x: x["page_num"])):
        # Merge if N/A and metadata matches previous
        if (page["category"] == "N/A" and prev and 
            page["dos"] == prev["dos"] and 
            page["facility"] == prev["facility"]):
            page["cluster_id"] = prev["cluster_id"]
        merged.append(page)
        prev = page

    return merged

def split_cluster_by_structure(pages):
    new_pages, new_cluster_id = [], 0
    pages = sorted(pages, key=lambda x: x["page_num"])
    prev_cat, prev_num = None, None

    for i, page in enumerate(pages):
        if i == 0:
            page["cluster_id"] = new_cluster_id
        else:
            if (page["category"] != prev_cat
                or abs(page["page_num"] - prev_num) > 1):
                new_cluster_id += 1
            page["cluster_id"] = new_cluster_id

        prev_cat, prev_num = page["category"], page["page_num"]
        new_pages.append(deepcopy(page))

    return new_pages

def group_pages(pdf_path):
    pages = extract_pages(pdf_path)
    cleaned_texts = [clean_text(p["text"]) for p in pages]
    embeddings = get_embeddings(cleaned_texts)
    cluster_labels = cluster_pages(embeddings)

    for i, page in enumerate(pages):
        page["cluster_id"] = cluster_labels[i]

    pages = carry_forward_metadata(pages)
    pages = merge_small_groups(pages)
    pages = merge_orphan_na(pages)
    pages = split_cluster_by_structure(pages)

    return pages
