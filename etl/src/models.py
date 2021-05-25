from typing import Union

from pydantic import BaseModel


class MovieViewingHistoryPayload(BaseModel):
    movie_timestamp: int
    movie_id: str
    user_id: str


class Event(BaseModel):
    payload: Union[MovieViewingHistoryPayload]
    language: str
    timezone: str
    fingerprint: dict
    ip: str
    type: str
    version: str
