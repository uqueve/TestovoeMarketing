from typing import List, Optional

from ..entities.search_entities import SearchParams, SearchQueryEntity
from ..repositories.search_repository import ISearchRepository


class GetSearchResultsUseCase:
    
    def __init__(self, repository: ISearchRepository):
        self.repository = repository
    
    def execute(self, params: SearchParams) -> SearchQueryEntity:
        search_query = self.repository.get_search_results(params)
        return self.repository.save_search_query(search_query)


class GetSearchQueryByIdUseCase:
    
    def __init__(self, repository: ISearchRepository):
        self.repository = repository
    
    def execute(self, query_id: int) -> Optional[SearchQueryEntity]:
        return self.repository.get_search_query_by_id(query_id)
