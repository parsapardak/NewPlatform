from django.urls import path
from .views import add_comment, add_reply

urlpatterns = [
    path('<int:news_id>/add/', add_comment, name='add-comment'),  # ارسال نظر
    path('<int:comment_id>/reply/', add_reply, name='add-reply'),  # پاسخ به نظر
]
