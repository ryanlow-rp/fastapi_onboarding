from pydantic import BaseModel, Field
from sqlalchemy import UniqueConstraint, Column, String


class ArtifactSchema(BaseModel):
    name: str
    element: str
    level: int


class ArtifactDB(ArtifactSchema):
    id: int
