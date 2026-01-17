from src.embedding_pipeline import EmbeddingPipeline
from src.retrieval_pipeline import DocumentRetriever
import pickle

class VectorStore:
    def __init__(self, model='intfloat/e5-small-v2'):
        self.model = model
        self.embedding_pipeline = EmbeddingPipeline()
        self.retriever = DocumentRetriever()

    def add_transcript(self, text, source_name, folder_path):
        docs = [{
            "text": text,
            "source": source_name
        }]
        
        chunks = self.embedding_pipeline.chunk_texts(docs, folder_path, type_source='audio')
        embeddings = self.embedding_pipeline.create_embeddings([chunk["text"] for chunk in chunks])
        self.embedding_pipeline.save_index(embeddings, folder_path)
        
    def search(self, query, base_dir, top_k=3):
        query_embedding = self.retriever.embed_query(query)
        matches_context = self.retriever.search(query_embedding, base_dir)
        return matches_context

    def get_by_id(self, folder_path, doc_id):
        with open(folder_path/"metadata.pkl", "rb") as f:
            metadata = pickle.load(f)

        docs = [m for m in metadata if m['source_id'] == doc_id]
        return docs
    
    def clear_index(self, folder_path):
        metadata_path = folder_path / "metadata.pkl"
        index_path = folder_path / "indexes.faiss"
        
        if metadata_path.exists():
            metadata_path.unlink()
        if index_path.exists():
            index_path.unlink()
        
        print("Index and metadata cleared")