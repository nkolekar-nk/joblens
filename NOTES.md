# JobLens – Learning Notes

## Checkpoint 1: Embeddings

### What an embedding is
An embedding turns text into a list of numbers (768 for nomic-embed-text) that represents its meaning,
so texts with similar meaning end up close together. "Close" is measured with cosine similarity:
the angle between two vectors, from -1 (opposite) to 1 (same direction).

> In my own words: _______________________________________________

### Experiment 1: Basic similarity
| Pair | Score |
|---|---|
| "I know Docker" vs "Containerization experience" | 0.472 |
| "Containerization experience" vs "Experience working with Python" | 0.472 |
| "I know Docker" vs "Experience working with Python" | 0.352 |
| "I know Docker" vs "I like pizza" | 0.338 |
| "built backend scripts" vs "I like pizza" | 0.253 (lowest) |

**What I learned**
- Docker and Containerization matched strongly with zero shared words, so embeddings capture meaning, not just keywords.
- Surprise: Containerization vs Python tied with Docker vs Containerization (0.472). Both contain "experience",
  so embeddings capture **wording and style**, not only topic.
- "I know Docker" vs "I like pizza" (0.338) was close to the tech pairs, likely because of the shared "I + verb + noun" structure.
- Absolute scores sit in a narrow band (~0.25–0.55). **Ranking matters more than the raw number**, which is why retrieval takes the top-k.

**Why it matters for RAG:** boilerplate words in job postings ("experience", "team", "benefits") can create false matches.
Short texts are noisy because a single word can dominate them.

### Experiment 2: nomic task prefixes
nomic-embed-text expects `search_query:` on queries and `search_document:` on documents.

| Query: "Docker experience" vs… | With prefixes | Without prefixes |
|---|---|---|
| Built and deployed containerized services | 0.430 | 0.517 |
| Experience writing Python scripts | 0.388 | 0.385 |
| I like pizza | 0.282 | 0.259 |
| **Gap (best − pizza)** | **0.148** | **0.258** |

**What I learned**
- With prefixes, the ranking was correct: the containerized-services document won without ever saying "Docker".
- Document-vs-document scores all jumped to ~0.5 (even vs pizza) because every document shared the `search_document:` prefix.
  **Shared text across chunks inflates similarity.** That doesn't affect retrieval, since only query-vs-document is compared.
- Decision: I will use prefixes in Checkpoint 3 because it helps with finding similarity between sentences more accurately.

### Python gotcha
Missing commas in a list silently merge strings (implicit string concatenation):
`["a" "b", "c"]` becomes `["ab", "c"]`. My sentences got glued together and gave misleading scores.

### Setup notes
- Chat model: llama3.2:3b (llama3.1 8B ran at ~4 tokens/s on my laptop, too slow for RAG prompts)
- llama3.2:3b: ~36 tokens/s to read the prompt, ~11 tokens/s to generate → about 40 seconds per RAG question
- Embedding model: nomic-embed-text (768 dimensions)
- Lesson: for RAG, the **prompt eval rate** matters most, because retrieved context makes prompts long.

## Interview-ready answers
- **What are embeddings?** Dense vectors representing meaning; similar texts map to nearby vectors.
- **Why cosine similarity?** It compares direction, not length, so it measures similarity of meaning regardless of text length.
- **A limitation?** Embeddings also capture surface wording. Shared boilerplate can create false matches.