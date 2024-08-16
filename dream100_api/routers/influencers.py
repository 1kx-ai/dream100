from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from dream100.db_config import get_db
from dream100.influencers.influencers import InfluencerContext
from dream100_api.schemas.influencer import Influencer, InfluencerCreate, InfluencerUpdate
from dream100_api.auth.dependencies import get_current_user
import pytest

router = APIRouter()

@router.get("/influencers", response_model=List[Influencer])
async def list_influencers(current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    influencer_context = InfluencerContext(db)
    influencers = influencer_context.list_influencers()
    return add_project_ids_to_influencers(influencers)

@router.post("/influencers", response_model=Influencer, status_code=status.HTTP_201_CREATED)
async def create_influencer(
    influencer: InfluencerCreate,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    influencer_context = InfluencerContext(db)
    new_influencer = influencer_context.create_influencer(name=influencer.name, project_ids=influencer.project_ids)
    return add_project_ids_to_influencer(new_influencer)

@router.get("/influencers/{influencer_id}", response_model=Influencer)
async def get_influencer(
    influencer_id: int,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    influencer_context = InfluencerContext(db)
    influencer = influencer_context.get_influencer(influencer_id)
    if not influencer:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Influencer not found")
    return add_project_ids_to_influencer(influencer)

@router.put("/influencers/{influencer_id}", response_model=Influencer)
async def update_influencer(
    influencer_id: int,
    influencer: InfluencerUpdate,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    influencer_context = InfluencerContext(db)
    updated_influencer = influencer_context.update_influencer(
        influencer_id, name=influencer.name, project_ids=influencer.project_ids
    )
    if not updated_influencer:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Influencer not found")
    return add_project_ids_to_influencer(updated_influencer)

@router.delete("/influencers/{influencer_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_influencer(
    influencer_id: int,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    influencer_context = InfluencerContext(db)
    success = influencer_context.delete_influencer(influencer_id)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Influencer not found")
    return

def add_project_ids_to_influencers(influencers):
    influencers = [add_project_ids_to_influencer(influencer) for influencer in influencers]
    return influencers

def add_project_ids_to_influencer(influencer):
    influencer.project_ids = [project.id for project in influencer.projects]
    return influencer