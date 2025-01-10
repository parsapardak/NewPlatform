from django.urls import path
from .views import register_page, login_user
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('register/', register_page, name='register'),
    path('login/', login_user, name='login'),
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),
]
