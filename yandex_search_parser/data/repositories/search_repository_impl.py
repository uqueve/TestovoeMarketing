from typing import List, Optional

from ...domain.entities.search_entities import SearchParams, SearchQueryEntity
from ...domain.repositories.search_repository import ISearchRepository
from ..datasources.xmlriver_datasource import XMLRiverDataSource
from ..datasources.django_orm_datasource import DjangoORMDataSource


class SearchRepositoryImpl(ISearchRepository):
    
    def __init__(self, 
                 datasource: XMLRiverDataSource = None, 
                 database: DjangoORMDataSource = None):
        self.datasource = datasource or XMLRiverDataSource()
        self.database = database or DjangoORMDataSource()
    
    def get_search_results(self, params: SearchParams) -> SearchQueryEntity:
        return self.datasource.get_search_results(params)
    
    def save_search_query(self, search_query: SearchQueryEntity) -> SearchQueryEntity:
        return self.database.save_search_query(search_query)
    
    def get_search_query_by_id(self, query_id: int) -> Optional[SearchQueryEntity]:
        return self.database.get_search_query_by_id(query_id)
