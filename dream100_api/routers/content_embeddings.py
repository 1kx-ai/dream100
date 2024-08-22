from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List
from dream100.db_config import get_db
from dream100_api.schemas.content_embedding import (
    ContentEmbedding,
    ContentEmbeddingSearch,
)
from dream100.context.content_embeddings import ContentEmbeddingContext
from dream100_api.auth.dependencies import get_current_user

router = APIRouter()


@router.get("/content_embeddings/list", response_model=List[ContentEmbedding])
async def list_content_embeddings(
    search: str = Query(None, description="Search query"),
    offset: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    context = ContentEmbeddingContext(db)

    # TODO: Implement the actual search logic here
    # For now, we'll just return a list of embeddings
    embeddings = context.list_embeddings(offset=offset, limit=limit)

    if not embeddings:
        raise HTTPException(status_code=404, detail="No content embeddings found")

    return embeddings
