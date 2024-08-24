from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from dream100.db_config import get_db
from dream100_api.schemas.content import ContentSearchResponse
from dream100.context.contents import ContentContext
from dream100.utilities.embedding_utils import create_embedding

router = APIRouter()


@router.get("/contents/search", response_model=ContentSearchResponse)
def search_contents(
    query: str, limit: int = 10, offset: int = 0, db: Session = Depends(get_db)
):
    content_context = ContentContext(db)
    query_embedding = create_embedding(query)
    results = content_context.search_contents(
        query_embedding, limit=limit, offset=offset
    )
    return ContentSearchResponse(**results)
