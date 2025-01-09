from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.hashers import make_password
from django.views.decorators.csrf import csrf_exempt
from .models import CustomUser
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
