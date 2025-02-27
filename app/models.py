from pydantic import BaseModel
from typing import Dict, Optional

class Event(BaseModel):
    event_type: str
    user_id: str
    timestamp: str
    metadata: Optional[Dict] = None

class ReportQuery(BaseModel):
    date_from: str
    date_to: str
    group_by: str