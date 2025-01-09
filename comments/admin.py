from django.contrib import admin
from .models import Comment


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['news', 'user', 'created_date']
    search_fields = ['content']
    list_filter = ['created_date', 'news']  # فیلتر بر اساس تاریخ و خبر
