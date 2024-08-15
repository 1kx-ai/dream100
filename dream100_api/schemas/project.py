from pydantic import BaseModel

class ProjectBase(BaseModel):
    name: str
    description: str = None

class ProjectCreate(ProjectBase):
    pass

class ProjectUpdate(ProjectBase):
    name: str = None
    description: str = None

class Project(ProjectBase):
    id: int

    class Config:
        orm_mode = True
