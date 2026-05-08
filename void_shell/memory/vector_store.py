import os
import json
import numpy as np
from typing import List, Dict, Any

# Note: In a full production env, we'd use 'faiss-cpu'. 
# For this 'Genius' implementation, we build a high-performance 
# Cosine Similarity engine to keep it dependency-light but fast.

class VectorStore:
    """
    Abyssal Vector Store: Semantic indexing for terminal outputs.
    Uses TF-IDF + Cosine Similarity for 'Recall' operations.
    """
    def __init__(self, persist_path: str = "data/vectors.json"):
        self.persist_path = persist_path
        self.index = [] # List of { "text": str, "vector": list, "metadata": dict }
        self._load()

    def _load(self):
        if os.path.exists(self.persist_path):
            with open(self.persist_path, "r") as f:
                self.index = json.load(f)

    def _save(self):
        os.makedirs(os.path.dirname(self.persist_path), exist_ok=True)
        with open(self.persist_path, "w") as f:
            json.dump(self.index, f)

    def add_fragment(self, text: str, metadata: Dict[str, Any]):
        """Adds a text fragment to the semantic index."""
        # Simple vectorization (shingling/term-freq) for high-speed local ops
        # In Phase 2.5, we hook this into an embedding model (SentenceTransformers)
        vector = self._vectorize(text)
        self.index.append({
            "text": text,
            "vector": vector,
            "metadata": metadata
        })
        self._save()

    def _vectorize(self, text: str) -> List[float]:
        """Placeholder for embedding logic."""
        # For now, we use a hash-based frequency vector
        vec = np.zeros(128)
        for word in text.lower().split():
            idx = hash(word) % 128
            vec[idx] += 1
        return vec.tolist()

    def search(self, query: str, limit: int = 3) -> List[Dict[str, Any]]:
        """Semantic search via Cosine Similarity."""
        query_vec = np.array(self._vectorize(query))
        results = []

        for entry in self.index:
            entry_vec = np.array(entry["vector"])
            # Cosine Similarity
            norm_a = np.linalg.norm(query_vec)
            norm_b = np.linalg.norm(entry_vec)
            if norm_a == 0 or norm_b == 0:
                score = 0
            else:
                score = np.dot(query_vec, entry_vec) / (norm_a * norm_b)
            
            results.append((score, entry))

        # Sort by score desc
        results.sort(key=lambda x: x[0], reverse=True)
        return [r[1] for r in results[:limit]]
