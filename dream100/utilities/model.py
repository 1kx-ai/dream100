from FlagEmbedding import FlagICLModel


class EmbeddingModel:
    _instance = None

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls._create_model()
        return cls._instance

    @staticmethod
    def _create_model():
        return FlagICLModel(
            "BAAI/bge-small-en-v1.5",
            query_instruction_for_retrieval="Given a web search query, retrieve relevant passages that answer the query.",
            examples_for_task=[
                {
                    "instruct": "Given a web search query, retrieve relevant passages that answer the query.",
                    "query": "what is a virtual interface",
                    "response": "A virtual interface is a software-defined abstraction that mimics the behavior and characteristics of a physical network interface. It allows multiple logical network connections to share the same physical network interface, enabling efficient utilization of network resources. Virtual interfaces are commonly used in virtualization technologies such as virtual machines and containers to provide network connectivity without requiring dedicated hardware. They facilitate flexible network configurations and help in isolating network traffic for security and management purposes.",
                },
                {
                    "instruct": "Given a web search query, retrieve relevant passages that answer the query.",
                    "query": "causes of back pain in female for a week",
                    "response": "Back pain in females lasting a week can stem from various factors. Common causes include muscle strain due to lifting heavy objects or improper posture, spinal issues like herniated discs or osteoporosis, menstrual cramps causing referred pain, urinary tract infections, or pelvic inflammatory disease. Pregnancy-related changes can also contribute. Stress and lack of physical activity may exacerbate symptoms. Proper diagnosis by a healthcare professional is crucial for effective treatment and management.",
                },
            ],
            use_fp16=True,
        )

    @classmethod
    def encode_queries(cls, queries):
        return cls.get_instance().encode_queries(queries)

    @classmethod
    def encode_corpus(cls, corpus):
        return cls.get_instance().encode_corpus(corpus)
