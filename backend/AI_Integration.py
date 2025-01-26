import numpy as np
from keybert import KeyBERT
from sentence_transformers import SentenceTransformer

def ai_function(prompt):
    print(f"Processing the prompt: {prompt}")  # Add this to check if the function is called

    res_model = SentenceTransformer("all-MiniLM-L6-v2")
    kw_model = KeyBERT()

    keywords = kw_model.extract_keywords(prompt, keyphrase_ngram_range=(1, 2), stop_words='english')
    keywords_array  = [kw[0] for kw in keywords]
    print("Extracted Keywords:", keywords_array)

    tags = [
        "hip-hop",
        "1990s",
        "festive",
        "jazz",
    ]


    # Generate embeddings
    embeddings1 = res_model.encode(keywords_array)
    embeddings2 = res_model.encode(tags)

    # Convert embeddings to NumPy arrays
    embeddings1 = np.array(embeddings1)
    embeddings2 = np.array(embeddings2)

    print(embeddings1.shape)
    print(embeddings2.shape)

    similarities = []


    for idx_i, keyword_embedding in enumerate(embeddings1):
        keyword_similarities = []
        for idx_j, tag_embedding in enumerate(embeddings2):
            # Compute similarity (cosine similarity or any similarity metric)
            similarity = np.dot(keyword_embedding, tag_embedding) / (np.linalg.norm(keyword_embedding) * np.linalg.norm(tag_embedding))
            keyword_similarities.append((tags[idx_j], round(similarity, 4)))  # Store similarity with tag name

        similarities.append((keywords_array[idx_i], keyword_similarities))  # Store similarities for the keyword

    # Organize results into a dictionary
    result = {}
    for keyword, keyword_similarities in similarities:
        result[keyword] = {tag: similarity for tag, similarity in keyword_similarities}

    print("Similarity Results:", result)  # Debug: Log the results
    return result