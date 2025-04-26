# page-clustering
# Page Clustering for Grouping Medical Records

This project clusters pages of multi-page PDF medical records based on their text and structure.  
It automatically identifies which pages belong to the same medical record group using NLP and clustering techniques.

## 🚀 Problem Statement
Given a large PDF file with many pages from different patients and hospitals,  
we need to group similar pages together into individual "medical records" without manual tagging.

## 🛠️ Tech Stack
- Python 3.10+
- Sentence-BERT (for text embeddings)
- DBSCAN clustering (unsupervised grouping)
- PDFPlumber (for extracting text from PDF pages)
- Pandas (for data handling)

## 📂 Project Structure

## 🧩 How It Works
1. Extract text from each page of the PDF.
2. Clean the text by removing noise.
3. Create embeddings using Sentence-BERT.
4. Cluster similar pages together using DBSCAN.
5. Assign each page a `cluster_id` representing a medical record group.
6. (Optional) Save results to CSV or display in a web app.

## 👩‍💻 How to Set Up
1. Clone the repository:
   ```bash
   git clone https://github.com/DhanyaSharma/page-clustering.git
   cd page-clustering
2. Create and activate a virtual environment:
    ```bash
    python -m venv venv
    .\venv\Scripts\activate  # On Windows
3. Install required libraries:
    ```bash
    pip install -r requirements.txt
4. Run sample scripts:
    To run the clustering:
    ```bash
    python src/clusterer.py
    To run the PDF text extraction:
    ```bash
    python src/pdf_extractor.py
