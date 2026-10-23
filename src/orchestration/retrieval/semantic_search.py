import torch
from sentence_transformers import SentenceTransformer, util


class SemanticSearch:
    def __init__(self, model_name="all-MiniLM-L6-v2"):
        self.model = SentenceTransformer(model_name)
        self.corpus = []
        self.corpus_embeddings = None

    def index_documents(self, documents):
        self.corpus = list(documents)
        self.corpus_embeddings = self.model.encode(self.corpus, convert_to_tensor=True)

    def search(self, query, top_k=5):
        if self.corpus_embeddings is None or not self.corpus:
            raise ValueError("No documents indexed. Call index_documents() first.")
        k = min(top_k, len(self.corpus))
        query_embedding = self.model.encode(query, convert_to_tensor=True)
        scores = util.pytorch_cos_sim(query_embedding, self.corpus_embeddings)[0]
        top_results = torch.topk(scores, k=k)
        return [
            (self.corpus[idx], score.item())
            for score, idx in zip(top_results.values, top_results.indices.tolist())
        ]