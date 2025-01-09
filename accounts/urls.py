from django.urls import path
from .views import register_page, login_user

urlpatterns = [
    path('register/', register_page, name='register'),
    path('login/', login_user, name='login'),
]
