from pydantic import BaseModel, ConfigDict
from typing import List, Optional

class InfluencerBase(BaseModel):
    name: str

class InfluencerCreate(InfluencerBase):
    project_ids: List[int]

class InfluencerUpdate(InfluencerBase):
    project_ids: Optional[List[int]] = None

class Influencer(InfluencerBase):
    id: int
    project_ids: List[int]

    model_config = ConfigDict(from_attributes=True)
