from django.urls import path
from .views import NewsView, NewsDetailView

urlpatterns = [
    path('', NewsView.as_view(), name='news-list'),
    path('<int:pk>/', NewsDetailView.as_view(), name='news-detail'),
]
