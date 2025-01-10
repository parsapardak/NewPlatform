from django.urls import path
from .views import user_profile, edit_profile, manage_users, register_page, login_user
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('register/', register_page, name='register'),
    path('login/', login_user, name='login'),
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),
    path('profile/', user_profile, name='user-profile'),
    path('profile/edit/', edit_profile, name='edit-profile'),
    path('users/manage/', manage_users, name='manage-users'),  # فقط برای سوپر یوزرها
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),
]
