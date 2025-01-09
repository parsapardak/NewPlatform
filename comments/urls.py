from django.urls import path
from .views import CommentView

urlpatterns = [
    path('<int:news_id>/add/', CommentView.as_view(), name='add-comment'),  # ارسال نظر
    path('<int:comment_id>/delete/', CommentView.as_view(), name='delete-comment'),  # حذف نظر
]
