from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from dream100.db_config import get_db
from dream100.web_properties.web_properties import WebPropertyContext
from dream100_api.schemas.web_property import WebProperty, WebPropertyCreate, WebPropertyUpdate

router = APIRouter()

@router.post("/web_properties", response_model=WebProperty, status_code=status.HTTP_201_CREATED)
async def create_web_property(
    web_property: WebPropertyCreate,
    db: Session = Depends(get_db),
):
    context = WebPropertyContext(db)
    try:
        new_web_property = context.create_web_property(
            influencer_id=web_property.influencer_id,
            type=web_property.type,
            url=web_property.url,
            followers=web_property.followers,
        )
        return new_web_property
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/web_properties/{web_property_id}", response_model=WebProperty)
async def get_web_property(
    web_property_id: int,
    db: Session = Depends(get_db),
):
    context = WebPropertyContext(db)
    web_property = context.get_web_property(web_property_id)
    if not web_property:
        raise HTTPException(status_code=404, detail="Web property not found")
    return web_property

@router.put("/web_properties/{web_property_id}", response_model=WebProperty)
async def update_web_property(
    web_property_id: int,
    web_property: WebPropertyUpdate,
    db: Session = Depends(get_db),
):
    context = WebPropertyContext(db)
    updated_web_property = context.update_web_property(
        web_property_id,
        type=web_property.type,
        url=web_property.url,
        followers=web_property.followers,
    )
    if not updated_web_property:
        raise HTTPException(status_code=404, detail="Web property not found")
    return updated_web_property

@router.delete("/web_properties/{web_property_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_web_property(
    web_property_id: int,
    db: Session = Depends(get_db),
):
    context = WebPropertyContext(db)
    if not context.delete_web_property(web_property_id):
        raise HTTPException(status_code=404, detail="Web property not found")
    return

@router.get("/web_properties", response_model=List[WebProperty])
async def list_web_properties(
    influencer_id: int = None,
    db: Session = Depends(get_db),
):
    context = WebPropertyContext(db)
    return context.list_web_properties(influencer_id=influencer_id)
