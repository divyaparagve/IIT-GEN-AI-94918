from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity


model = SentenceTransformer("all-MiniLM-L6-v2")
  # 384 dimensions

sentences = [
    "I love football",
    "Soccer is my favorite sport",
    "I enjoy cooking pasta"
]

# Generate embeddings
embeddings = model.encode(sentences)

# cosine_similarity requires 2D arrays
sim_1_2 = cosine_similarity(
    [embeddings[0]],
    [embeddings[1]]
)[0][0]

sim_1_3 = cosine_similarity(
    [embeddings[0]],
    [embeddings[2]]
)[0][0]

print("Similarity (football vs soccer):", sim_1_2)
print("Similarity (football vs cooking):", sim_1_3)

