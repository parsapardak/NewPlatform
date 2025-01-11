from django.urls import path
from .views import user_profile, edit_profile, manage_users, register_page, login_user, change_user_role, edit_user_profile
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('register/', register_page, name='register'),
    path('login/', login_user, name='login'),
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),
    path('profile/', user_profile, name='user-profile'),
    path('users/manage/', manage_users, name='manage-users'),
    path('profile/edit/', edit_profile, name='edit-profile'),  # ویرایش پروفایل خود
    path('users/<int:user_id>/edit/', edit_user_profile, name='edit-user-profile'),  # ویرایش پروفایل کاربران دیگر
    path('users/<int:user_id>/change-role/', change_user_role, name='change-user-role'), 
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),
]
