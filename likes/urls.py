from django.urls import path
from .views import LikeView

urlpatterns = [
    path('<int:news_id>/like/', LikeView.as_view(), name='like-news'),
    path('<int:news_id>/unlike/', LikeView.as_view(), name='unlike-news'),
]
