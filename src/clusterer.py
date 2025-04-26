from sentence_transformers import SentenceTransformer
import hdbscan
import numpy as np

# Load a pre-trained model (you can also try 'all-MiniLM-L6-v2' or 'clinicalBERT')
model = SentenceTransformer('all-MiniLM-L6-v2')

def get_embeddings(cleaned_texts):
    """Converts list of cleaned texts to sentence embeddings"""
    return model.encode(cleaned_texts, show_progress_bar=True)

def cluster_pages(embeddings):
    """Groups pages based on their embeddings"""
    clusterer = hdbscan.HDBSCAN(min_cluster_size=2)
    cluster_labels = clusterer.fit_predict(embeddings)
    return cluster_labels

# Sample test
if __name__ == "__main__":
    sample_texts = [
        "lab report patient abc date jan 1 2024",
        "test result: hemoglobin normal",
        "progress note patient abc january 2",
        "follow-up for flu symptoms",
        "lab report patient xyz jan 3 2024"
    ]

    # Example cleaning
    from text_cleaner import clean_text
    cleaned = [clean_text(t) for t in sample_texts]

    # Generate embeddings & cluster
    embeddings = get_embeddings(cleaned)
    clusters = cluster_pages(embeddings)

    for i, (text, cluster_id) in enumerate(zip(sample_texts, clusters)):
        print(f"Page {i+1}: Cluster {cluster_id} - {text}")
