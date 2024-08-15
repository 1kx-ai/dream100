from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from dream100.db_config import create_session
from dream100.projects.projects import ProjectContext
from dream100_api.auth.dependencies import get_current_user

router = APIRouter()

def get_db():
    db, _ = create_session()
    try:
        yield db
    finally:
        db.close()

@router.get("/projects")
async def list_projects(current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    project_context = ProjectContext(db)
    projects = project_context.list_projects()
    return {"projects": [{"id": p.id, "name": p.name} for p in projects]}