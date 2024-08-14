from sqlalchemy import Column, Integer, ForeignKey, Text, Index
from sqlalchemy.orm import relationship
from dream100.db_config import Base
from dream100.models.content import Content
from pgvector.sqlalchemy import Vector
from sqlalchemy.orm import mapped_column

class ContentEmbedding(Base):
    __tablename__ = 'content_embeddings'

    id = Column(Integer, primary_key=True)
    content_id = Column(Integer, ForeignKey('contents.id'), nullable=False)
    chunk_text = Column(Text, nullable=False)
    embedding = mapped_column(Vector(384))  # Adjust the dimension to match your model's output

    content = relationship("Content", back_populates="embeddings")

    def __repr__(self):
        return f"<ContentEmbedding(id={self.id}, content_id={self.content_id})>"

# Add an approximate index
embedding_index = Index(
    'content_embedding_index',
    ContentEmbedding.embedding,
    postgresql_using='hnsw',
    postgresql_with={'m': 16, 'ef_construction': 64},
    postgresql_ops={'embedding': 'vector_cosine_ops'}
)

# Update the Content model to include the relationship
Content.embeddings = relationship("ContentEmbedding", back_populates="content")