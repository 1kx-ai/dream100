from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from dream100.db_config import get_db
from dream100_api.schemas.content import ContentSearchResponse, Content
from dream100.context.contents import ContentContext
from dream100.utilities.embedding_utils import create_embedding
from typing import Optional

router = APIRouter()

@router.get("/content/{content_id}", response_model=Content)
def get_content(
    content_id: int,
    db: Session = Depends(get_db)
):
    content_context = ContentContext(db)
    content = content_context.get_content(content_id)
    if content is None:
        raise HTTPException(status_code=404, detail="Content not found")
    return content


@router.get("/contents/search", response_model=ContentSearchResponse)
def search_contents(
    query: str,
    project_id: Optional[int] = Query(None, description="Filter results by project ID"),
    per_page: int = Query(10, ge=1, le=100),
    page: int = Query(0, ge=0),
    db: Session = Depends(get_db),
):
    content_context = ContentContext(db)
    query_embedding = create_embedding(query)
    results = content_context.search_contents(
        query_embedding, project_id=project_id, per_page=per_page, page=page
    )
    return ContentSearchResponse(**results)
