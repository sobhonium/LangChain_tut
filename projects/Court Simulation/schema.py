from typing import Optional, List, TypedDict
from pydantic import BaseModel, Field

class GraphState(TypedDict):
    history: Optional[List[str]]
    turn: Optional[str]
    max_iter: Optional[int]
    topic: Optional[str]
    current_iter: Optional[int]

class ArbiterQuestion(BaseModel):
    target_speaker: str = Field(..., description="One of: 'first speaker', 'second speaker', or 'third speaker'")
    question: str = Field(..., description="A single follow-up question addressed to the target speaker")
