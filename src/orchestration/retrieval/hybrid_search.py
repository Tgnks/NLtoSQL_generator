from semantic_search import SemanticSearch
from vector_search import VectorSearch

class HybridSearch:
    def __init__(self, semantic_model, vector_model):
        self.semantic_search = SemanticSearch(semantic_model)
        self.vector_search = VectorSearch(vector_model)

    def search(self, query, top_k=10):
        semantic_results = self.semantic_search.search(query, top_k)
        vector_results = self.vector_search.search(query, top_k)

        combined_results = self.combine_results(semantic_results, vector_results)
        return combined_results

    def combine_results(self, semantic_results, vector_results):
        # Combine and rank results from both searches
        combined = {result['id']: result for result in semantic_results}

        for result in vector_results:
            if result['id'] not in combined:
                combined[result['id']] = result
            else:
                combined[result['id']]['score'] += result['score']

        # Sort combined results by score
        sorted_results = sorted(combined.values(), key=lambda x: x['score'], reverse=True)
        return sorted_results[:10]  # Return top 10 results