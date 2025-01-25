from keybert import KeyBERT
from sentence_transformers import SentenceTransformer 

res_model = SentenceTransformer("all-MiniLM-L6-v2")
kw_model = KeyBERT()

keywords = kw_model.extract_keywords("make a playlist of chill jazz songs from the 90s", keyphrase_ngram_range=(1, 2), stop_words='english')
keywords_array  = [kw[0] for kw in keywords]
print("Extracted Keywords:", keywords_array)

tags = [
    "hip-hop",
    "1990s",
    "festive",
    "jazz",
]

embeddings1 = res_model.encode(keywords_array)
embeddings2 = res_model.encode(tags)

similarities = res_model.similarity(embeddings1, embeddings2)

for idx_i, keyword in enumerate(keywords_array):
    print(keyword)
    for idx_j, tag in enumerate(tags):
        print(f" - {tag: <30}: {similarities[idx_i][idx_j]:.4f}")
