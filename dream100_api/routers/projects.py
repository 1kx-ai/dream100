from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from dream100.db_config import create_session
from dream100.projects.projects import ProjectContext
from dream100_api.auth.dependencies import get_current_user
from dream100_api.schemas.project import Project, ProjectCreate, ProjectUpdate

router = APIRouter()

def get_db():
    db, _ = create_session()
    try:
        yield db
    finally:
        db.close()

@router.get("/projects", response_model=list[Project]) 
async def list_projects(current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    project_context = ProjectContext(db)
    projects = project_context.list_projects()
    return projects                                                                                                      
                                                                                                                          
@router.post("/projects", response_model=Project, status_code=status.HTTP_201_CREATED)                                   
async def create_project(                                                                                                
     project: ProjectCreate,                                                                                              
     current_user: dict = Depends(get_current_user),                                                                      
     db: Session = Depends(get_db),                                                                                       
 ):                                                                                                                       
     project_context = ProjectContext(db)                                                                                 
     new_project = project_context.create_project(name=project.name, description=project.description)                     
     return new_project                                                                                                   
                                                                                                                          
@router.get("/projects/{project_id}", response_model=Project)                                                            
async def get_project(                                                                                                   
     project_id: int,                                                                                                     
     current_user: dict = Depends(get_current_user),                                                                      
     db: Session = Depends(get_db),                                                                                       
 ):                                                                                                                       
     project_context = ProjectContext(db)                                                                                 
     project = project_context.get_project(project_id)                                                                    
     if not project:                                                                                                      
         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")                           
     return project                                                                                                       
                                                                                                                          
@router.put("/projects/{project_id}", response_model=Project)                                                            
async def update_project(                                                                                                
     project_id: int,                                                                                                     
     project: ProjectUpdate,                                                                                              
     current_user: dict = Depends(get_current_user),                                                                      
     db: Session = Depends(get_db),                                                                                       
 ):                                                                                                                       
     project_context = ProjectContext(db)                                                                                 
     updated_project = project_context.update_project(                                                                    
         project_id, name=project.name, description=project.description                                                   
     )                                                                                                                    
     if not updated_project:                                                                                              
         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")                           
     return updated_project                                                                                               
                                                                                                                          
@router.delete("/projects/{project_id}", status_code=status.HTTP_204_NO_CONTENT)                                         
async def delete_project(                                                                                                
     project_id: int,                                                                                                     
     current_user: dict = Depends(get_current_user),                                                                      
     db: Session = Depends(get_db),                                                                                       
 ):                                                                                                                       
     project_context = ProjectContext(db)                                                                                 
     success = project_context.delete_project(project_id)                                                                 
     if not success:                                                                                                      
         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")                           
     return
