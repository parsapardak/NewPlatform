from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.hashers import make_password
from .models import CustomUser

def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        phone = request.POST.get('phone')

        if not username or not password or not phone:
            return JsonResponse({'error': 'All fields are required'}, status=400)

        if CustomUser.objects.filter(username=username).exists():
            return JsonResponse({'error': 'Username already exists'}, status=400)

        user = CustomUser.objects.create(
            username=username,
            password=make_password(password),
            email=f"{username}@example.com",  # ایمیل آزمایشی
            user_type='registered'
        )
        user.save()

        return JsonResponse({'message': 'User registered successfully!'}, status=201)
    return JsonResponse({'error': 'Invalid request method'}, status=405)
