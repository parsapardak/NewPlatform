from django.urls import path
from .views import NewsView, NewsDetailView, create_news

urlpatterns = [
    path('', NewsView.as_view(), name='news_list'),
    path('<int:pk>/', NewsDetailView.as_view(), name='news_detail'),  # نمایش جزئیات خبر
    path('create/', create_news, name='create_news'),  # ایجاد خبر جدید
]
