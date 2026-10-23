from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

class VectorSearch:
    def __init__(self, embeddings):
        self.embeddings = embeddings

    def search(self, query_embedding, top_k=5):
        similarities = cosine_similarity(query_embedding.reshape(1, -1), self.embeddings)
        similar_indices = np.argsort(similarities[0])[::-1][:top_k]
        return similar_indices, similarities[0][similar_indices]

# Example usage:
# embeddings = np.array([[...], [...], ...])  # Load or generate your embeddings here
# vector_search = VectorSearch(embeddings)
# query_embedding = np.array([...])  # Generate the embedding for your query
# results = vector_search.search(query_embedding)