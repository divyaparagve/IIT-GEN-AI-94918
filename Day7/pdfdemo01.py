import numpy as np
def cosine_similarity(a, b):
 return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))
cat = np.array([0.2, 0.9, 0.1])
dog = np.array([0.25, 0.85, 0.15])
car = np.array([-0.8, 0.1, 0.9])
print("cat vs dog:", cosine_similarity(cat, dog)) # ~1 (close)
print("cat vs car:", cosine_similarity(cat, car)) # ~0 or negative (far)