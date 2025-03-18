import requests
import xml.etree.ElementTree as ET
from django.conf import settings
from datetime import datetime
from bs4 import BeautifulSoup

from ...domain.entities.search_entities import SearchParams, SearchQueryEntity, SearchResultEntity


class XMLRiverDataSource:
    """API для работы с XMLRiver"""
    
    BASE_URL = "http://xmlriver.com/search_yandex/xml"
    
    def __init__(self):
        self.api_key = settings.XMLRIVER_API_KEY
        self.user = settings.XMLRIVER_USER
    
    def get_search_results(self, params: SearchParams) -> SearchQueryEntity:
        request_params = {
            "user": self.user,
            "key": self.api_key,
            "query": params.keyword.replace("&", "%26"),
            "device": "desktop" if params.device.lower() == "десктоп" else params.device.lower(),
            "lr": self._get_lr_for_location(params.location),
        }
        
        response = requests.get(self.BASE_URL, params=request_params)
        response.raise_for_status()
        
        search_query = SearchQueryEntity(
            keyword=params.keyword,
            location=params.location,
            device=params.device,
            created_at=datetime.now(),
            results=[]
        )
        
        try:
            soup = BeautifulSoup(response.text, 'lxml')
            docs = soup.find_all('doc')
            
            for doc in docs:
                url = doc.find('url').text
                title = doc.find('title').text
                content_type = doc.find('contenttype').text

                search_query.results.append(
                    SearchResultEntity(
                        title=title,
                        url=url,
                        result_type=content_type,
                        created_at=datetime.now()
                    )
                )
        except Exception as e:
            print(f"Ошибка при парсинге XML: {str(e)}")
        
        return search_query
    
    def _get_lr_for_location(self, location: str) -> int:
        location_codes = {
            "Москва": 213,
            "Санкт-Петербург": 2,
            "Новосибирск": 65,
            "Екатеринбург": 54,
            "Казань": 43,
            "Нижний Новгород": 47,
            "Челябинск": 56,
            "Омск": 66,
            "Самара": 51,
            "Ростов-на-Дону": 39,
            "Уфа": 172,
            "Красноярск": 62,
            "Воронеж": 193,
            "Пермь": 50,
            "Волгоград": 38,
        }
        
        return location_codes.get(location, 213) 