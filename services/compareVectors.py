from typing import List

from sklearn.metrics.pairwise import cosine_similarity
from numpy import array

def compareVectorsService(vectors: List[List[float]]) -> float:
    if len(vectors) != 2:
        raise ValueError('Only two vectors for compare')

    vector_a, vector_b = array([vectors[0]]), array([vectors[1]])

    if vector_a.shape != vector_b.shape:
        raise ValueError('Vectors must have the same dimensions')

    if vector_a.size == 0:
        return 0.0

    similarity = cosine_similarity(vector_a, vector_b)
    return round(float(similarity[0][0]), 2)
