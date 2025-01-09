from django.contrib import admin

# Register your models here.
from .models import AskModel

# Регистрация модели Ask_Model в админке
@admin.register(AskModel)
class AskModelAdmin(admin.ModelAdmin):
    list_display = ('question', 'answer', 'created_at', 'updated_at')  # Отображаемые столбцы
    search_fields = ('question', 'answer')  # Поля для поиска
    list_filter = ('created_at', 'updated_at')  # Фильтры по дате
    ordering = ('-created_at',)  # Сортировка по дате создания, от новых к старым