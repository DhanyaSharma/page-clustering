import streamlit as st
from src.group_pages import group_pages
from src.output_writer import save_to_csv
from src.summarizer import summarize_groups
import os
import tempfile


st.set_page_config(page_title="Medical Record Grouper", layout="wide")
st.title("📄 Medical Page Clustering & Grouping")


# Upload
uploaded_file = st.file_uploader("Upload a multi-page medical PDF", type=["pdf"])

def save_uploaded_file(uploaded_file):
    temp_dir = tempfile.mkdtemp()
    file_path = os.path.join(temp_dir, uploaded_file.name)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    return file_path

if uploaded_file is not None:
    with st.spinner("🔍Grouping.... please wait."):
        try:
            # Save file
            pdf_path = save_uploaded_file(uploaded_file)

            # Run grouping pipeline
            pages = group_pages(pdf_path)

            # Save CSV
            save_to_csv(pages)

            # Show group summary
            summary_df = summarize_groups(pages)
            st.subheader("📊 Group Summary Table")
            st.dataframe(summary_df)

            # Download CSV
            csv = summary_df.to_csv(index=False).encode('utf-8')
            st.download_button("📥 Download Summary as CSV", csv, "summary.csv", "text/csv")

            # Color-coding for categories
            color_map = {
                "Lab Report": "#e6f7ff",  # Blue
                "Progress Note": "#fffbe6",  # Yellow
                "Discharge Summary": "#e6ffe6",  # Green
                "Medication List": "#fff0f0",  # Red
            }

            # Show grouped records with color coding
            grouped = {}
            for page in pages:
                grouped.setdefault(page["cluster_id"], []).append(page)

            # Display "Grouped Medical Records" header with a large font
            st.markdown("<h2 style='font-size:30px;'>📂 Grouped Medical Records</h2>", unsafe_allow_html=True)

            # Loop through the grouped records
            for cluster_id in sorted(grouped.keys()):
                st.markdown(f"<h3 style='font-size:24px;'>🗂️ Record Group {cluster_id} ({len(grouped[cluster_id])} pages)</h3>", unsafe_allow_html=True)
                
                for page in grouped[cluster_id]:
                    # Get color based on category
                    bg_color = color_map.get(page["category"], "#f9f9f9")  # Default gray if not found
                    
                    # Create a layout for metadata side-by-side with background color
                    st.markdown(f"""
                        <div style="background-color:{bg_color}; padding:15px; border-radius:10px; margin-bottom:15px; display: flex; flex-wrap: wrap;">
                            <div style="flex: 1 1 45%; padding-right: 20px;">
                                <b>Page {page['page_num']}</b><br>
                                <b>Category:</b> {page['category']}<br>
                                <b>Provider(s):</b> {page['provider'] or 'N/A'}<br>
                                <b>Date of Service:</b> {page['dos'] or 'N/A'}<br>
                                <b>Facility:</b> {page['facility'] or 'N/A'}
                            </div>
                        </div>
                    """, unsafe_allow_html=True)

        except Exception as e:
            st.error(f"❌ Error while processing the file: {e}")
