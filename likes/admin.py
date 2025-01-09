from django.contrib import admin
from .models import Like


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ['news', 'user', 'created_date']
    list_filter = ['created_date']
