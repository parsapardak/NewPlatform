from django.urls import path
from .views import add_comment, add_reply, edit_comment, delete_comment

urlpatterns = [
    path('<int:news_id>/add/', add_comment, name='add-comment'),  # ارسال نظر
    path('<int:comment_id>/reply/', add_reply, name='add-reply'),  # پاسخ به نظر
    path('<int:comment_id>/edit/', edit_comment, name='edit-comment'),
    path('<int:comment_id>/delete/', delete_comment, name='delete-comment'),

]
