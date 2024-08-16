import numpy as np
from ..content_embeddings.model import EmbeddingModel


def create_embedding(text):
    if not isinstance(text, str):
        text = str(text)
    embedding = EmbeddingModel.encode_queries([text])[0]
    return embedding.tolist()


def create_corpus_embedding(text):
    if not isinstance(text, str):
        text = str(text)
    embedding = EmbeddingModel.encode_corpus([text])[0]
    return embedding.tolist()


def chunk_content(content, chunk_size=512, overlap=50):
    words = content.split()
    chunks = []
    for i in range(0, len(words), chunk_size - overlap):
        chunk = " ".join(words[i : i + chunk_size])
        chunks.append(chunk)
    return chunks


def batch_create_embeddings(texts):
    texts = [str(text) for text in texts]
    embeddings = EmbeddingModel.encode_corpus(texts)
    return embeddings.tolist()


def compute_similarity(query_embedding, corpus_embeddings):
    query_embedding = np.array(query_embedding)
    corpus_embeddings = np.array(corpus_embeddings)
    similarity = query_embedding @ corpus_embeddings.T
    return similarity.tolist()
