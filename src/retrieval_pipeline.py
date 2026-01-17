from sentence_transformers import SentenceTransformer
import faiss
import pickle

class DocumentRetriever:
    def __init__(self, model = 'intfloat/e5-small-v2'):
        self.model = SentenceTransformer(model)

    def embed_query(self, query):
        query = f"query: {query}"
        embedding = self.model.encode(
            [query],
            normalize_embeddings=True
        )
        return embedding.astype("float32")
    
    def search(self, query, folder_path, top_k=3):
        index = faiss.read_index(str(folder_path / "indexes.faiss"))
        with open(folder_path/"metadata.pkl", "rb") as f:
            metadata = pickle.load(f)

        D, I = index.search(query, top_k)

        results = []
        for i in I[0]:
            results.append(metadata[i])

        return results
    
    