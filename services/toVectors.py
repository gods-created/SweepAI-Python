from typing import List

from sklearn.feature_extraction.text import TfidfVectorizer

def toVectorsService(code1: str, code2: str) -> List[List[float]]:
    corpus = [str(code1), str(code2)]
    vectorizer = TfidfVectorizer()

    try:
        embeddings = vectorizer.fit_transform(corpus)
    except ValueError:
        return [[0.0], [0.0]]

    return embeddings.toarray().tolist()