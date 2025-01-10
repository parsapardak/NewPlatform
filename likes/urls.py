from django.urls import path
from .views import LikeNewsView, UnlikeNewsView

urlpatterns = [
    path('<int:news_id>/like/', LikeNewsView.as_view(), name='like-news'),  # لایک کردن خبر
    path('<int:news_id>/unlike/', UnlikeNewsView.as_view(), name='unlike-news'),  # لغو لایک خبر
]
