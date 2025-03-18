from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages

from yandex_search_parser.domain.entities.search_entities import SearchParams
from yandex_search_parser.domain.use_cases.search_use_cases import (
    GetSearchResultsUseCase,
    GetSearchQueryByIdUseCase,
)
from yandex_search_parser.data.repositories.search_repository_impl import SearchRepositoryImpl
from yandex_search_parser.models import SearchQuery
from yandex_search_parser.tasks import parse_yandex_search


class SearchView(View):
    
    def get(self, request):
        return render(request, 'yandex_search_parser/search_form.html')
    
    def post(self, request):
        keyword = request.POST.get('keyword')
        location = request.POST.get('location', 'Москва')
        device = request.POST.get('device', 'десктоп')
        
        if not keyword:
            messages.error(request, 'Пожалуйста, введите ключевое слово')
            return redirect('search')
        
        search_params = SearchParams(
            keyword=keyword,
            location=location,
            device=device
        )
        
        # Сюда можно пробросить другой репозиторий и реализацию работы с апи
        repository = SearchRepositoryImpl()
        use_case = GetSearchResultsUseCase(repository)
        
        try:
            search_query = use_case.execute(search_params)
            messages.success(request, f'Найдено {len(search_query.results)} результатов')
            
            db_query = SearchQuery.objects.filter(
                keyword=keyword,
                location=location,
                device=device
            ).order_by('-created_at').first()
            
            if db_query:
                return redirect('search_results', query_id=db_query.id)
            else:
                messages.error(request, 'Не удалось сохранить результаты поиска')
                return redirect('search')
                
        except Exception as e:
            messages.error(request, f'Ошибка при выполнении поиска: {str(e)}')
            return redirect('search')


class SearchResultsView(View):
    
    def get(self, request, query_id):
        repository = SearchRepositoryImpl()
        use_case = GetSearchQueryByIdUseCase(repository)
        search_query = use_case.execute(query_id)
        
        if not search_query:
            messages.error(request, 'Поисковый запрос не найден')
            return redirect('search')
        
        return render(request, 'yandex_search_parser/search_results.html', {
            'search_query': search_query
        })


class RunTaskView(View):
    
    def get(self, request):
        return render(request, 'yandex_search_parser/run_task.html')
    
    def post(self, request):
        keyword = request.POST.get('keyword', 'кредит наличными быстро')
        location = request.POST.get('location', 'Москва')
        device = request.POST.get('device', 'desktop')
        
        task = parse_yandex_search.delay(keyword, location, device)
        
        messages.success(request, f'Задача запущена (ID: {task.id}). Результаты будут сохранены в базе данных.')
        return redirect('search')
