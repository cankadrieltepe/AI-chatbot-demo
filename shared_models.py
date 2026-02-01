from __future__ import annotations
from dataclasses import dataclass
from typing import List, Optional, Literal
from pydantic import BaseModel, Field

MachineType = Literal[
    "washing_machine",
    "refrigerator",
    "dishwasher",
    "vacuum",
    "microwave",
    "air_conditioner",
    "other"
]

ComplaintType = Literal[
    "not_powering_on",
    "leak",
    "noise",
    "not_cooling_or_heating",
    "not_cleaning_well",
    "bad_smell_smoke_burning",
    "error_code",
    "performance_slow",
    "other"
]

@dataclass
class RouterDeps:
    # kept for future expansion
    pass

class RouterResult(BaseModel):
    machine_type: MachineType
    complaint_types: List[ComplaintType] = Field(default_factory=list)
    urgency: int = Field(..., ge=1, le=5, description="1=low, 5=high danger/urgent")
    short_summary: str = Field(..., description="One-sentence summary in English")
    clarifying_questions: List[str] = Field(default_factory=list)

@dataclass
class SafetyDeps:
    user_text: str
    machine_type: MachineType
    complaint_types: List[ComplaintType]
    urgency: int

class SafetyResult(BaseModel):
    allowed_to_provide_steps: bool
    must_include_safety_warning: bool
    escalation_recommended: bool
    safety_warning_text: Optional[str] = None
    required_questions: List[str] = Field(default_factory=list)

@dataclass
class ExpertDeps:
    user_text: str
    machine_type: MachineType
    complaint_types: List[ComplaintType]
    urgency: int
    required_questions: List[str]
    must_include_safety_warning: bool
    safety_warning_text: Optional[str]

class ExpertResult(BaseModel):
    final_reply: str
    checklist: List[str] = Field(default_factory=list)
    questions_to_ask: List[str] = Field(default_factory=list)
