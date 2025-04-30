import streamlit as st
from src.group_pages import group_pages
from src.output_writer import save_to_csv
import tempfile

st.set_page_config(page_title="Medical PDF Clustering", layout="wide")
st.title("📄 Grouping Medical Records Tool")

st.write("""
This tool reads a medical PDF document and groups related pages together — such as lab reports, doctor's notes, and follow-up records — so you can understand which pages belong to the same medical case or visit.
""")

pdf_file = st.file_uploader("Upload a medical PDF file", type=["pdf"])

if pdf_file:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(pdf_file.read())
        tmp_path = tmp.name

    st.info("🔍Grouping.... please wait.")
    try:
        pages = group_pages(tmp_path)
    except Exception as e:
        st.error(f"❌ Error while processing the file: {e}")
        st.stop()

    if not pages:
        st.warning("⚠️ No text found in the PDF.")
        st.stop()

    save_to_csv(pages)
    st.success("✅ Pages grouped successfully! Results saved to `grouped_pages.csv`")

    import pandas as pd
    df = pd.read_csv("grouped_pages.csv")
    st.download_button("📥 Download Grouped CSV", df.to_csv(index=False), file_name="grouped_pages.csv")

    # Group pages by cluster ID
    from collections import defaultdict
    cluster_map = defaultdict(list)
    for page in pages:
        cluster_map[page['cluster_id']].append(page)

    st.markdown("### 📂 Grouped Medical Records")
    for cluster_id, cluster_pages in cluster_map.items():
        with st.expander(f"🗂️ Record Group {cluster_id} ({len(cluster_pages)} page{'s' if len(cluster_pages) > 1 else ''})", expanded=False):
            for page in cluster_pages:
                st.markdown(f"**Page {page['pagenumber']}**")
                st.write(f"**Category:** {page.get('category', 'N/A')}")
                st.write(f"**Provider(s):** {page.get('providers', 'N/A')}")
                st.write(f"**Date of Service:** {page.get('dos', 'N/A')}")
                st.write(f"**Facility:** {page.get('facility', 'N/A')}")
