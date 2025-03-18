from abc import ABC, abstractmethod
from typing import List, Optional

from ..entities.search_entities import SearchQueryEntity, SearchParams, SearchResultEntity


class ISearchRepository(ABC):
    
    @abstractmethod
    def get_search_results(self, params: SearchParams) -> SearchQueryEntity:
        pass
    
    @abstractmethod
    def save_search_query(self, search_query: SearchQueryEntity) -> SearchQueryEntity:
        pass
    
    @abstractmethod
    def get_search_query_by_id(self, query_id: int) -> Optional[SearchQueryEntity]:
        pass
