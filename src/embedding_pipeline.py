from sentence_transformers import SentenceTransformer
import fitz
import faiss
import pickle
from tqdm import tqdm
import re

def clean_text(text):
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

class EmbeddingPipeline:
    def __init__(self, model = 'intfloat/e5-small-v2'):
        self.model = SentenceTransformer(model)

    def chunk_texts(self, docs, folder_path, type_source: str = 'docs', max_tokens=400, overlap=50):
        chunks = []
        tokenizer = self.model.tokenizer
        
        metadata_path = folder_path / "metadata.pkl"
        existing_chunks = []
        max_source_id = -1

        if metadata_path.exists():
            with open(metadata_path, "rb") as f:
                existing_chunks = pickle.load(f)
            
            if existing_chunks:
                max_source_id = max(chunk["source_id"] for chunk in existing_chunks)

        for i, doc in enumerate(docs):
            source_id = max_source_id + 1 + i

            tokens = tokenizer(
                doc["text"],
                add_special_tokens=False,
                return_attention_mask=False
            )["input_ids"]

            start = 0
            chunk_num = 1
            while start < len(tokens):
                end = start + max_tokens
                chunk_tokens = tokens[start:end]
                chunk_text = tokenizer.decode(chunk_tokens)
                
                chunks.append({
                    "source_id": source_id,
                    "source": doc["source"],
                    "type_source": type_source,
                    "chunk": chunk_num,
                    "text": "passage: " + chunk_text
                })

                start += max_tokens - overlap
                chunk_num += 1

        print(f"Created {len(chunks)} chunks")

        all_chunks = existing_chunks + chunks
    
        with open(metadata_path, "wb") as f:
            pickle.dump(all_chunks, f)

        return chunks
    
    def create_embeddings(self, chunks: list): #from chunks['text'] only
        embeddings = self.model.encode(
            chunks,
            batch_size=32,
            normalize_embeddings=True,
            show_progress_bar=True
        ).astype("float32")
        print("Created embeddings")
        return embeddings
        
    
    def save_index(self, embeddings: list, folder_path):
        dim = embeddings.shape[1]
        index_path = folder_path / "indexes.faiss"

        if index_path.exists():
            index = faiss.read_index(str(index_path))
        else:
            index = faiss.IndexFlatIP(dim)

        index.add(embeddings)
        faiss.write_index(index, str(index_path))

        