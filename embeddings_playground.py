import numpy as np
import ollama 

def embed(text):
    resp = ollama.embed(model="nomic-embed-text", input = text)
    return np.array(resp["embeddings"][0])

def cosine(a, b):
    return a @ b /(np.linalg.norm(a) * np.linalg.norm(b))

sentences = [
    "search_query: Docker experience",
    "search_document: Built and deployed containerized services",
    "search_document: Experience writing Python scripts",
    "search_document: I like pizza",
]
vecs = [embed(s) for s in sentences]
print("Vector length:", len(vecs[0]))

for i in range(len(sentences)):
    for j in range(i+1, len(sentences)):
        print(f"{sentences[i]!r} vs {sentences[j]!r}: {cosine(vecs[i], vecs[j]):.3f}")