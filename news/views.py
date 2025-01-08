from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views import View
from .models import News
from accounts.models import CustomUser

@method_decorator(login_required, name='dispatch')
class NewsView(View):
    def get(self, request):
        news_list = News.objects.all()
        return JsonResponse({'news': list(news_list.values())}, safe=False)

    def post(self, request):
        if request.user.user_type not in ['admin', 'superuser']:
            return JsonResponse({'error': 'Permission denied'}, status=403)

        title = request.POST.get('title')
        content = request.POST.get('content')

        if not title or not content:
            return JsonResponse({'error': 'All fields are required'}, status=400)

        news = News.objects.create(
            title=title,
            content=content,
            author=request.user
        )
        return JsonResponse({'message': 'News created successfully!', 'id': news.id}, status=201)

@method_decorator(login_required, name='dispatch')
class NewsDetailView(View):
    def get(self, request, pk):
        news = get_object_or_404(News, pk=pk)
        return JsonResponse({'id': news.id, 'title': news.title, 'content': news.content})

    def put(self, request, pk):
        if request.user.user_type not in ['admin', 'superuser']:
            return JsonResponse({'error': 'Permission denied'}, status=403)

        news = get_object_or_404(News, pk=pk)
        news.title = request.PUT.get('title', news.title)
        news.content = request.PUT.get('content', news.content)
        news.save()

        return JsonResponse({'message': 'News updated successfully!'})

    def delete(self, request, pk):
        if request.user.user_type not in ['admin', 'superuser']:
            return JsonResponse({'error': 'Permission denied'}, status=403)

        news = get_object_or_404(News, pk=pk)
        news.delete()
        return JsonResponse({'message': 'News deleted successfully!'})
