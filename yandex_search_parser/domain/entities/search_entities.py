from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class SearchParams:
    keyword: str
    location: str
    device: str


@dataclass
class SearchResultEntity:
    title: str
    url: str
    result_type: str
    created_at: datetime | None = None


@dataclass
class SearchQueryEntity:
    keyword: str
    location: str
    device: str
    created_at: datetime | None = None
    results: list[SearchResultEntity] = field(default_factory=list)
