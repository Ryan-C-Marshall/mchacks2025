import numpy as np
from keybert import KeyBERT
from sentence_transformers import SentenceTransformer
from backend.data_manipulation import get_association_words
import backend.data_manipulation as data_manipulation

def ai_function(prompt):
    print(f"Processing the prompt: {prompt}")  # Add this to check if the function is called

    res_model = SentenceTransformer("all-MiniLM-L6-v2")
    kw_model = KeyBERT()

    keywords = kw_model.extract_keywords(prompt, keyphrase_ngram_range=(1, 2), stop_words='english')
    keywords_array  = [kw[0] for kw in keywords]
    print("Extracted Keywords:", keywords_array)


    tags = get_association_words()



    # Generate embeddings
    embeddings1 = res_model.encode(keywords_array)
    embeddings2 = res_model.encode(tags)


    # Convert embeddings to NumPy arrays
    embeddings1 = np.array(embeddings1)
    embeddings2 = np.array(embeddings2)


    print(embeddings1.shape)
    print(embeddings2.shape)

    similarities = []


    for idx_i, tag_embedding in enumerate(embeddings2):
        tag_similarities = []
        for idx_j, keyword_embedding in enumerate(embeddings1):
            similarity = np.dot(tag_embedding, keyword_embedding) / (np.linalg.norm(tag_embedding) * np.linalg.norm(keyword_embedding))
            tag_similarities.append((keywords_array[idx_j], round(similarity, 4)))  # Store similarity with tag name

        similarities.append((tags[idx_i], tag_similarities))  # Store similarities for the keyword

    # Organize results into a dictionary
    result = {}
    for tag, tag_similarities in similarities:
        # result[tag] = {keyword: round(float(similarity),2) for keyword, similarity in tag_similarities}
        result[tag] = max([round(float(similarity),2) for _, similarity in tag_similarities])

    print(result)  # Debug: Log the results

    # print("Similarity Results:", result)  # Debug: Log the results

    return data_manipulation.rank_songs(result)