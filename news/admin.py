from django.contrib import admin
from .models import News


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'published_date', 'likes_count']
    search_fields = ['title', 'content', 'author__username', 'summary']
    list_filter = ['published_date', 'author']
