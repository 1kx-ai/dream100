from pydantic import BaseModel, ConfigDict


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

    model_config = ConfigDict(from_attributes=True)
