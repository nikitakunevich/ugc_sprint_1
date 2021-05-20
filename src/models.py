from datetime import datetime
from typing import Union

from pydantic import BaseModel


class MovieViewingHistoryPayload(BaseModel):
    timestamp: int
    movie_id: int
    user_id: int


class Event(BaseModel):
    payload: Union[MovieViewingHistoryPayload]
    timestamp: int = datetime.now().timestamp()
    language: str
    timezone: str
    fingerprint: dict
    ip: str
    type: str
    version: str
