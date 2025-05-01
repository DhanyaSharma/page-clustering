from sentence_transformers import SentenceTransformer
from sklearn.cluster import DBSCAN
from src.text_cleaner import clean_text


# Load the Sentence-BERT model
model = SentenceTransformer('all-MiniLM-L6-v2')

def get_embeddings(cleaned_texts):
    """Converts list of cleaned texts to sentence embeddings"""
    return model.encode(cleaned_texts, show_progress_bar=True)

def cluster_pages(embeddings, eps=0.4, min_samples=2):
    db = DBSCAN(eps=eps, min_samples=min_samples, metric='cosine')
    return db.fit_predict(embeddings)


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
    cleaned = [clean_text(t) for t in sample_texts]

    # Generate embeddings
    embeddings = get_embeddings(cleaned)

    # Cluster the embeddings
    clusters = cluster_pages(embeddings)

    # Print out cluster labels
    for i, (text, cluster_id) in enumerate(zip(sample_texts, clusters)):
        print(f"Page {i+1}: Cluster {cluster_id} - {text}")
