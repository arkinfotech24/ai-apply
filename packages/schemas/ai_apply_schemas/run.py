from pydantic import BaseModel, Field
from typing import Any, Dict, List, Optional, Literal
from enum import Enum

class RunStatus(str, Enum):
    CREATED = "CREATED"
    ASSIGNED = "ASSIGNED"
    RUNNING = "RUNNING"
    WAITING_FOR_USER = "WAITING_FOR_USER"
    SUCCEEDED = "SUCCEEDED"
    FAILED = "FAILED"
    CANCELED = "CANCELED"

class AgentInfo(BaseModel):
    agent_id: str
    user_id: str
    hostname: Optional[str] = None
    platform: Optional[str] = None
    version: Optional[str] = None

class AgentRegisterRequest(BaseModel):
    agent_id: str
    user_id: str
    hostname: Optional[str] = None
    platform: Optional[str] = None
    version: Optional[str] = None

class AgentHeartbeatRequest(BaseModel):
    agent_id: str

class Receipt(BaseModel):
    confirmation_text: Optional[str] = None
    confirmation_number: Optional[str] = None
    applied_url: Optional[str] = None
    applied_at: Optional[str] = None  # ISO8601

class ArtifactRef(BaseModel):
    kind: Literal["screenshot","html","pdf","docx","text","other"]
    path: str
    content_type: Optional[str] = None

class RunEventIn(BaseModel):
    ts: str  # ISO8601
    event_type: str
    step_id: Optional[str] = None
    message: Optional[str] = None
    data: Dict[str, Any] = Field(default_factory=dict)

class RunPayload(BaseModel):
    run_id: str
    user_id: str
    apply_url: str
    platform_hint: Optional[str] = None
    mode: str = "REVIEW_FIRST"
    field_payload: Dict[str, Any] = Field(default_factory=dict)
    answers: Dict[str, Any] = Field(default_factory=dict)
    documents: List[ArtifactRef] = Field(default_factory=list)

class AgentPollResponse(BaseModel):
    run: Optional[RunPayload] = None

class RunCreateRequest(BaseModel):
    job_id: str
    mode: str = "REVIEW_FIRST"

class RunCompleteRequest(BaseModel):
    status: RunStatus
    receipt: Optional[Receipt] = None
    artifacts: List[ArtifactRef] = Field(default_factory=list)
    events: List[RunEventIn] = Field(default_factory=list)
    errors: List[Dict[str, Any]] = Field(default_factory=list)
