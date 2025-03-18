from typing import List, Optional
from django.db.models import Prefetch

from ...models import SearchQuery, SearchResult
from ...domain.entities.search_entities import SearchQueryEntity, SearchResultEntity


class DjangoORMDataSource:
    
    def save_search_query(self, search_query: SearchQueryEntity) -> SearchQueryEntity:
        db_query = SearchQuery.objects.create(
            keyword=search_query.keyword,
            location=search_query.location,
            device=search_query.device
        )
        
        for result in search_query.results:
            SearchResult.objects.create(
                search_query=db_query,
                title=result.title,
                url=result.url,
                result_type=result.result_type,
            )
        
        return search_query
    
    def get_search_query_by_id(self, query_id: int) -> Optional[SearchQueryEntity]:
        try:
            query = SearchQuery.objects.prefetch_related(
                Prefetch('results')
            ).get(id=query_id)
            
            results = []
            for result in query.results.all():
                results.append(SearchResultEntity(
                    title=result.title,
                    url=result.url,
                    result_type=result.result_type,
                    created_at=result.created_at
                ))
            
            return SearchQueryEntity(
                keyword=query.keyword,
                location=query.location,
                device=query.device,
                created_at=query.created_at,
                results=results
            )
        except SearchQuery.DoesNotExist:
            return None
