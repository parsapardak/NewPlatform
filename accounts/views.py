from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.hashers import make_password
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import CustomUser
from news.models import News
import re  # برای بررسی فرمت شماره موبایل


def register_page(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        email = request.POST.get('email')
        phone = request.POST.get('phone')

        # بررسی خالی نبودن فیلدها
        if not username or not password or not confirm_password or not email or not phone:
            messages.error(request, 'All fields are required.')
            return redirect('register')

        # بررسی تطابق رمز عبور
        if password != confirm_password:
            messages.error(request, 'Passwords do not match.')
            return redirect('register')

        # بررسی فرمت ایمیل
        if '@' not in email or '.' not in email:
            messages.error(request, 'Invalid email address.')
            return redirect('register')

        # بررسی شماره تماس
        if not phone.isdigit() or len(phone) != 11:
            messages.error(request, 'Invalid phone number format.')
            return redirect('register')

        # بررسی یکتایی نام کاربری و ایمیل
        if CustomUser.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists.')
            return redirect('register')
        if CustomUser.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists.')
            return redirect('register')

        # ایجاد کاربر جدید
        try:
            user = CustomUser.objects.create(
                username=username,
                email=email,
                phone=phone,
                password=make_password(password)
            )
            user.save()
            messages.success(request, 'Registration successful! Please log in.')
            return redirect('login')
        except Exception as e:
            messages.error(request, f'Error creating account: {str(e)}')
            return redirect('register')

    return render(request, 'accounts/register.html')



def login_user(request):
    if request.method == 'POST':
        # دریافت داده‌های فرم
        username = request.POST.get('username')
        password = request.POST.get('password')

        # بررسی اینکه هیچ فیلدی خالی نباشد
        if not username or not password:
            messages.error(request, 'Both username and password are required!')
            return redirect('login')

        # احراز هویت کاربر
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome back, {user.username}!')
            return redirect('/')
        else:
            messages.error(request, 'Invalid username or password!')
            return redirect('login')

    # بازگشت فرم در درخواست GET
    return render(request, 'accounts/login.html')



@login_required
def user_profile(request):
    """
    نمایش اطلاعات پروفایل بر اساس نوع کاربر
    """
    if request.user.user_type == 'superuser':
        # نمایش پروفایل سوپریوزر همراه با لیست کاربران
        users = CustomUser.objects.all()

        return render(request, 'accounts/profile_superuser.html', {
            'user': request.user,
            'users': users,
        })

    elif request.user.user_type == 'admin':
        admin_news = News.objects.filter(author=request.user)
        return render(request, 'accounts/profile_admin.html', {
            'user': request.user,
            'admin_news': admin_news,
        })

    else:
        # نمایش پروفایل کاربر عادی همراه با کامنت‌ها
        user_comments = request.user.comment_set.all()  # کامنت‌های ثبت‌شده توسط کاربر
        return render(request, 'accounts/profile_user.html', {
            'user': request.user,
            'user_comments': user_comments
        })


@login_required
def edit_profile(request):
    """
    ویرایش اطلاعات پروفایل کاربر
    """
    if request.method == 'POST':
        user = request.user
        user.username = request.POST.get('username', user.username)
        user.email = request.POST.get('email', user.email)
        user.phone = request.POST.get('phone', user.phone)

        if 'password' in request.POST and request.POST['password']:
            user.set_password(request.POST['password'])

        user.save()
        messages.success(request, 'Your profile has been updated successfully!')
        return redirect('user-profile')

    return render(request, 'accounts/edit_profile.html', {'user': request.user})


@login_required
def manage_users(request):
    """
    مدیریت کاربران (مخصوص سوپریوزرها)
    """
    if request.user.user_type != 'superuser':
        messages.error(request, 'You do not have permission to access this page.')
        return redirect('user-profile')

    # جست‌وجو و فیلتر کاربران
    query = request.GET.get('search', '')
    user_type_filter = request.GET.get('user_type', '')
    users = CustomUser.objects.all()

    if query:
        users = users.filter(username__icontains=query)

    if user_type_filter:
        users = users.filter(user_type=user_type_filter)

    return render(request, 'accounts/manage_users.html', {
        'users': users,
        'search_query': query,
        'user_type_filter': user_type_filter,
    })



@login_required
def change_user_role(request, user_id):
    """
    تغییر نقش کاربر (مخصوص سوپریوزرها)
    """
    if request.user.user_type != 'superuser':
        messages.error(request, 'You do not have permission to access this page.')
        return redirect('user-profile')

    user = get_object_or_404(CustomUser, id=user_id)

    if request.method == 'POST':
        new_role = request.POST.get('user_type')
        if new_role in ['registered', 'admin', 'superuser']:
            user.user_type = new_role
            user.save()
            messages.success(request, f'Role of {user.username} updated to {new_role}.')
        else:
            messages.error(request, 'Invalid role selected.')

        return redirect('manage-users')

    return render(request, 'accounts/change_user_role.html', {'user': user})



@login_required
def edit_user_profile(request, user_id):
    """
    ویرایش اطلاعات پروفایل سایر کاربران (فقط توسط سوپریوزر)
    """
    if request.user.user_type != 'superuser':
        messages.error(request, 'You do not have permission to edit other users.')
        return redirect('user-profile')

    user = get_object_or_404(CustomUser, id=user_id)

    if request.method == 'POST':
        user.username = request.POST.get('username', user.username)
        user.email = request.POST.get('email', user.email)
        user.phone = request.POST.get('phone', user.phone)
        if 'password' in request.POST and request.POST['password']:
            user.set_password(request.POST['password'])
        user.save()
        messages.success(request, f'{user.username}\'s profile updated successfully!')
        return redirect('user-profile')

    return render(request, 'accounts/edit_profile.html', {'user': user})
