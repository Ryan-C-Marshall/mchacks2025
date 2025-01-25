from sentence_transformers import SentenceTransformer 

model = SentenceTransformer("all-MiniLM-L6-v2")

keywords = [
    "rap",
    "90s",
    "Christmas",
    "pop"
]

tags = [
    "hip-hop",
    "1990s",
    "festive",
    "rock"
]

embeddings1 = model.encode(keywords)
embeddings2 = model.encode(tags)

similarities = model.similarity(embeddings1, embeddings2)

for idx_i, keyword in enumerate(keywords):
    print(keyword)
    for idx_j, tag in enumerate(tags):
        print(f" - {tag: <30}: {similarities[idx_i][idx_j]:.4f}")
