import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from groq import Groq

model = SentenceTransformer("all-MiniLM-L6-v2")
client = Groq(api_key="YOUR_GROQ_API_KEY")

class DatasetRAG:
    def __init__(self):
        self.texts = []
        self.index = None
        self.memory = []

    def add_texts(self, texts):
        self.texts.extend(texts)

    def build_index(self):
        vectors = model.encode(self.texts)

        dim = vectors.shape[1]
        self.index = faiss.IndexFlatL2(dim)
        self.index.add(np.array(vectors))

    def search(self, query, k=5):
        q = model.encode([query])
        _, idx = self.index.search(np.array(q), k)
        return [self.texts[i] for i in idx[0]]

    def ask(self, query):
        context = self.search(query)
        history = "\n".join(self.memory[-6:])

        prompt = f"""
You are a legal AI assistant.

History:
{history}

Context:
{context}

Question:
{query}

Answer clearly and highlight risks or violations.
"""

        res = client.chat.completions.create(
            model="llama3-70b-8192",
            messages=[{"role": "user", "content": prompt}]
        )

        ans = res.choices[0].message.content

        self.memory.append(f"User: {query}")
        self.memory.append(f"AI: {ans}")

        return ans
