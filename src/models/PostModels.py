from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel, Field, constr, field_validator


class PostLinks(BaseModel):
    links: list[str] = Field(min_length=1)
    tags: str = Field(min_length=1)


class PostMetaData(BaseModel):
    manga_title: constr(max_length=255)
    manga_site: constr(max_length=255)
    manga_url: constr(min_length=1)
    manga_image: constr(min_length=1)
    en_manga_image: Optional[str]
    manga_rating: float

    @classmethod
    @field_validator('manga_rating')
    def validate_rating(cls, value):
        if not 0.0 <= value <= 5.0:
            raise ValueError("Manga rating must be between 0 and 5")
        return value

    manga_genre: List[str]
    manga_type: constr(max_length=255)
    manga_release: Optional[datetime]
    manga_status: constr(max_length=255)
    date_added: datetime


class PostChapters(BaseModel):
    manga_url: str = Field(min_length=1)
