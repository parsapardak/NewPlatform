from django.urls import path
from .views import NewsView, NewsDetailView, create_news, edit_news, delete_news

urlpatterns = [
    path('', NewsView.as_view(), name='news_list'),
    path('<int:pk>/', NewsDetailView.as_view(), name='news_detail'),  # نمایش جزئیات خبر
    path('create/', create_news, name='create_news'),  # ایجاد خبر جدید
    path('<int:pk>/delete/', delete_news, name='delete-news'),
    path('<int:pk>/edit/', edit_news, name='edit-news'),
]

