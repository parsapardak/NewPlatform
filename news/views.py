from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views import View
from .models import News


@method_decorator(login_required, name='dispatch')
class NewsView(View):
    def get(self, request):
        """
        نمایش لیست خبرها
        """
        news_list = News.objects.all().order_by('-published_date').values(
            'id', 'title', 'content', 'author__username', 'published_date', 'likes_count', 'comments_count'
        )
        return JsonResponse({'news': list(news_list)}, safe=False)

    def post(self, request):
        """
        ایجاد خبر جدید توسط کاربران ادمین یا ارشد
        """
        if request.user.user_type not in ['admin', 'superuser']:
            return JsonResponse({'error': 'Permission denied'}, status=403)

        title = request.POST.get('title')
        content = request.POST.get('content')

        if not title or not content:
            return JsonResponse({'error': 'All fields are required'}, status=400)

        try:
            news = News.objects.create(
                title=title,
                content=content,
                author=request.user
            )
            return JsonResponse({'message': 'News created successfully!', 'id': news.id}, status=201)
        except Exception as e:
            return JsonResponse({'error': f'Error creating news: {str(e)}'}, status=500)


@method_decorator(login_required, name='dispatch')
class NewsDetailView(View):
    def get(self, request, pk):
        """
        نمایش جزئیات یک خبر
        """
        news = get_object_or_404(News, pk=pk)
        return JsonResponse({
            'id': news.id,
            'title': news.title,
            'content': news.content,
            'author': news.author.username,
            'published_date': news.published_date.strftime('%Y-%m-%d %H:%M:%S'),
            'likes_count': news.likes_count,
            'comments_count': news.comments_count
        })

    def put(self, request, pk):
        """
        ویرایش یک خبر
        """
        if request.user.user_type not in ['admin', 'superuser']:
            return JsonResponse({'error': 'Permission denied'}, status=403)

        try:
            news = get_object_or_404(News, pk=pk)
            title = request.POST.get('title', news.title)
            content = request.POST.get('content', news.content)

            if not title or not content:
                return JsonResponse({'error': 'All fields are required'}, status=400)

            news.title = title
            news.content = content
            news.save()
            return JsonResponse({'message': 'News updated successfully!'})
        except Exception as e:
            return JsonResponse({'error': f'Error updating news: {str(e)}'}, status=500)

    def delete(self, request, pk):
        """
        حذف یک خبر
        """
        if request.user.user_type not in ['admin', 'superuser']:
            return JsonResponse({'error': 'Permission denied'}, status=403)

        try:
            news = get_object_or_404(News, pk=pk)
            news.delete()
            return JsonResponse({'message': 'News deleted successfully!'})
        except Exception as e:
            return JsonResponse({'error': f'Error deleting news: {str(e)}'}, status=500)


@login_required
def create_news(request):
    """
    ویو برای ایجاد خبر از طریق فرم
    """
    if request.user.user_type not in ['admin', 'superuser']:
        return render(request, 'news/error.html', {'error': 'Permission denied'})

    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')

        if not title or not content:
            return render(request, 'news/create_news.html', {'error': 'All fields are required'})

        try:
            news = News.objects.create(
                title=title,
                content=content,
                author=request.user
            )
            return redirect('news_list')
        except Exception as e:
            return render(request, 'news/create_news.html', {'error': f'Error creating news: {str(e)}'})

    return render(request, 'news/create_news.html')






def get(self, request):
    search_query = request.GET.get('search', '')
    sort_by = request.GET.get('sort', '-published_date')

    news_list = News.objects.all()

    # جست‌وجو
    if search_query:
        news_list = news_list.filter(
            models.Q(title__icontains=search_query) |
            models.Q(content__icontains=search_query)
        )

    # مرتب‌سازی
    if sort_by == 'likes':
        news_list = news_list.order_by('-likes_count')
    else:
        news_list = news_list.order_by(sort_by)

    return JsonResponse({'news': list(news_list.values(
        'id', 'title', 'author__username', 'published_date', 'likes_count'
    ))}, safe=False)
