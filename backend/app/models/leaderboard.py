from pydantic import BaseModel
from datetime import datetime
from typing import List

class LeaderboardEntry(BaseModel):
    user_id: str
    username: str
    ppg: float
    rank: int

class Leaderboard(BaseModel):
    id: str # Represents the window, e.g., "1d", "7d"
    updated_at: datetime
    entries: List[LeaderboardEntry]
