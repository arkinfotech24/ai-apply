from pydantic import BaseModel, Field
from typing import List, Optional

class JobImportRequest(BaseModel):
    url: Optional[str] = None
    pasted_description: Optional[str] = None

class JobExtract(BaseModel):
    title: Optional[str] = None
    company: Optional[str] = None
    location: Optional[str] = None
    remote_type: Optional[str] = Field(default=None, description="remote|hybrid|onsite")
    employment_type: Optional[str] = None
    requirements: List[str] = Field(default_factory=list)
    nice_to_have: List[str] = Field(default_factory=list)
    keywords: List[str] = Field(default_factory=list)
