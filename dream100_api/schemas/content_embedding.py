from pydantic import BaseModel
from typing import List

class ContentEmbeddingBase(BaseModel):
    content_id: int
    chunk_text: str
    embedding: List[float]

class ContentEmbeddingCreate(ContentEmbeddingBase):
    pass

class ContentEmbedding(ContentEmbeddingBase):
    id: int

    class Config:
        orm_mode = True

class ContentEmbeddingUpdate(BaseModel):
    chunk_text: str | None = None
    embedding: List[float] | None = None

class ContentEmbeddingSearch(BaseModel):
    query_embedding: List[float]
    limit: int = 5
    offset: int = 0
