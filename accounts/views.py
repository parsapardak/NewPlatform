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
        # دریافت داده‌های فرم
        username = request.POST.get('username')
        password = request.POST.get('password')
        phone = request.POST.get('phone')

        # بررسی اینکه هیچ فیلدی خالی نباشد
        if not username or not password or not phone:
            return render(request, 'accounts/register.html', {'error': 'All fields are required'})

        # بررسی فرمت شماره موبایل
        if not re.match(r'^09\d{9}$', phone):
            return render(request, 'accounts/register.html', {'error': 'Invalid phone number format'})

        # بررسی اینکه شماره موبایل تکراری نباشد
        if CustomUser.objects.filter(phone=phone).exists():
            return render(request, 'accounts/register.html', {'error': 'Phone number already exists'})

        # بررسی اینکه نام کاربری تکراری نباشد
        if CustomUser.objects.filter(username=username).exists():
            return render(request, 'accounts/register.html', {'error': 'Username already exists'})

        # ایجاد کاربر جدید
        try:
            user = CustomUser.objects.create(
                username=username,
                password=make_password(password),
                phone=phone,
                user_type='registered'
            )
            user.save()
            return redirect('login')  # بازگشت به صفحه ورود
        except Exception as e:
            return render(request, 'accounts/register.html', {'error': f'Error creating user: {str(e)}'})

    # بازگشت فرم در درخواست GET
    return render(request, 'accounts/register.html')


def login_user(request):
    if request.method == 'POST':
        # دریافت داده‌های فرم
        username = request.POST.get('username')
        password = request.POST.get('password')

        # بررسی اینکه هیچ فیلدی خالی نباشد
        if not username or not password:
            return render(request, 'accounts/login.html', {'error': 'Both username and password are required'})

        # احراز هویت کاربر
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/')  # بازگشت به صفحه اصلی پس از لاگین
        else:
            return render(request, 'accounts/login.html', {'error': 'Invalid username or password'})

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
        messages.success(request, 'Profile updated successfully!')
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
