import numpy as np
import ollama 

def embed(text):
    resp = ollama.embed(model="nomic-embed-text", input = text)
    return np.array(resp["embeddings"][0])

def cosine(a, b):
    return a @ b /(np.linalg.norm(a) * np.linalg.norm(b))

sentences = [
    "Docker experience",
    "Built and deployed containerized services",
    "Experience writing Python scripts",
    "I like pizza",
]
vecs = [embed(s) for s in sentences]
print("Vector length:", len(vecs[0]))

for i in range(len(sentences)):
    for j in range(i+1, len(sentences)):
        print(f"{sentences[i]!r} vs {sentences[j]!r}: {cosine(vecs[i], vecs[j]):.3f}")