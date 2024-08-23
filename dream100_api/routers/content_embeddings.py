from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from dream100.db_config import get_db
from dream100_api.schemas.content_embedding import (
    ContentEmbedding,
    ContentEmbeddingSearch,
    PaginatedContentEmbeddings,
)
from dream100.context.content_embeddings import ContentEmbeddingContext
from dream100_api.auth.dependencies import get_current_user
from dream100.utilities.embedding_utils import create_embedding

router = APIRouter()


@router.get("/content_embeddings/list", response_model=PaginatedContentEmbeddings)
async def list_content_embeddings(
    search: Optional[str] = Query(None, description="Search query"),
    query: Optional[str] = Query(None, description="Query for semantic search"),
    content_id: Optional[int] = Query(None, description="Filter by content ID"),
    page: int = Query(1, ge=1, description="Page number"),
    per_page: int = Query(10, ge=1, le=100, description="Items per page"),
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    context = ContentEmbeddingContext(db)

    query_embedding = None
    if query:
        query_embedding = create_embedding(query)

    embeddings = context.list_embeddings(
        content_id=content_id,
        query_embedding=query_embedding,
        search=search,
        page=page,
        per_page=per_page,
    )

    total_count = context.get_embedding_count(content_id=content_id)

    if not embeddings:
        raise HTTPException(status_code=404, detail="No content embeddings found")

    return PaginatedContentEmbeddings(
        items=embeddings,
        total=total_count,
        page=page,
        per_page=per_page,
    )
