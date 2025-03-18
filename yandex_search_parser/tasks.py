from celery import shared_task
from celery.result import AsyncResult

from yandex_search_parser.data.repositories.search_repository_impl import SearchRepositoryImpl
from yandex_search_parser.domain.entities.search_entities import SearchParams


@shared_task
def parse_yandex_search(keyword: str, location: str, device: str) -> str:
    try:
        search_params = SearchParams(keyword=keyword, location=location, device=device)
        search_service = SearchRepositoryImpl()
        search_query = search_service.get_search_results(search_params)
        search_service.save_search_query(search_query)
        return True
    except Exception as e:
        print(f'Ошибка при выполнении задачи: {e}')
        return False


@shared_task(name="parse_yandex_search_schedule")
def parse_yandex_search_schedule(keyword="купить автомобиль", location="Москва", device="desktop"):
    parse_yandex_search.delay(keyword, location, device)
