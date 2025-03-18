from django.db import models
from django.utils import timezone


class SearchQuery(models.Model):
    keyword = models.CharField(max_length=255, verbose_name="Ключевое слово")
    location = models.CharField(max_length=100, verbose_name="Геолокация")
    device = models.CharField(max_length=50, verbose_name="Устройство")
    created_at = models.DateTimeField(default=timezone.now, verbose_name="Дата создания")
    
    class Meta:
        verbose_name = "Поисковый запрос"
        verbose_name_plural = "Поисковые запросы"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.keyword} - {self.location} - {self.device}"


class SearchResult(models.Model):
    RESULT_TYPES = (
        ('organic', 'Органическая выдача'),
        ('ad', 'Реклама'),
    )
    
    search_query = models.ForeignKey(SearchQuery, on_delete=models.CASCADE, related_name='results', verbose_name="Поисковый запрос")
    title = models.CharField(max_length=500, verbose_name="Заголовок")
    url = models.URLField(max_length=1000, verbose_name="URL")
    result_type = models.CharField(max_length=20, choices=RESULT_TYPES, verbose_name="Тип результата")
    created_at = models.DateTimeField(default=timezone.now, verbose_name="Дата создания")
    
    class Meta:
        verbose_name = "Результат поиска"
        verbose_name_plural = "Результаты поиска"
    
    def __str__(self):
        return f"{self.title[:50]}... ({self.result_type})"
