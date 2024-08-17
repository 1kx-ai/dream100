import numpy as np


class MockEmbeddingModel:
    @staticmethod
    def encode_queries(queries):
        return np.array([create_float_array(384) for _ in queries])

    @staticmethod
    def encode_corpus(corpus):
        return np.array([create_float_array(384) for _ in corpus])


def create_float_array(n, offset=0.0):
    """
    Create an array of float values from offset to (n-1) * 0.1 + offset, with a step of 0.1.

    :param n: The number of elements in the array
    :param offset: The starting value for the array (default is 0.0)
    :return: A list of float values
    """
    return [round(i * 0.1 + offset, 1) for i in range(n)]
