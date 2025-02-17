from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views import View
from django.db.models import Q, Count
from .models import News
from comments.models import Comment


class NewsView(View):
    def get(self, request):
        """
        نمایش لیست خبرها (برای کاربران مهمان و لاگین‌شده)
        """
        # دریافت پارامترهای جست‌وجو و مرتب‌سازی
        search_query = request.GET.get('search', '')
        sort_by = request.GET.get('sort', '-published_date')

        # دریافت لیست خبرها با شمارش تعداد نظرات
        news_list = News.objects.annotate(comments_count=Count('comments'))

        # جست‌وجو در عنوان و محتوا
        if search_query:
            news_list = news_list.filter(
                Q(title__icontains=search_query) |
                Q(content__icontains=search_query)
            )

        # مرتب‌سازی بر اساس تعداد لایک‌ها یا تاریخ انتشار
        if sort_by == 'likes':
            news_list = sorted(news_list, key=lambda x: x.likes.count(), reverse=True)
        else:
            news_list = news_list.order_by(sort_by)

        # ارسال داده‌ها به قالب HTML
        return render(request, 'news/news_list.html', {
            'news': news_list
        })


class NewsDetailView(View):
    def get(self, request, pk):
        """
        نمایش جزئیات یک خبر (برای کاربران مهمان و لاگین‌شده)
        """
        # دریافت خبر مورد نظر
        news = get_object_or_404(News, pk=pk)

        # مرتب‌سازی نظرات
        sort = request.GET.get('sort', 'newest')
        if sort == 'oldest':
            comments = Comment.objects.filter(news=news).order_by('created_date')
        else:
            comments = Comment.objects.filter(news=news).order_by('-created_date')

    
        # دریافت نظرات مرتبط با خبر
        comments = Comment.objects.filter(news=news).order_by('-created_date')

        # ارسال داده‌ها به قالب HTML
        return render(request, 'news/news_details.html', {
            'news': news,
            'comments': comments,
        })


@login_required
def create_news(request):
    """
    ویو برای ایجاد خبر از طریق فرم (فقط برای ادمین‌ها)
    """
    if request.user.user_type not in ['admin', 'superuser']:
        return render(request, 'news/error.html', {'error': 'Permission denied'})

    if request.method == 'POST':
        title = request.POST.get('title')
        summary = request.POST.get('summary')
        content = request.POST.get('content')
        image = request.FILES.get('image')

        if not title or not content:
            return render(request, 'news/create_news.html', {'error': 'All fields are required'})

        try:
            news = News.objects.create(
                title=title,
                summary=summary,
                content=content,
                author=request.user,
                image=image,           
            )
            return redirect('news_list')
        except Exception as e:
            return render(request, 'news/create_news.html', {'error': f'Error creating news: {str(e)}'})

    return render(request, 'news/create_news.html')


@login_required
def delete_news(request, pk):
    """
    ویو برای حذف خبر (فقط توسط ادمین‌ها و سوپرکاربرها)
    """
    if request.user.user_type not in ['admin', 'superuser']:
        return render(request, 'news/error.html', {'error': 'Permission denied'})

    news = get_object_or_404(News, pk=pk)

    if request.method == 'POST':
        news.delete()
        return redirect('news_list')

    return render(request, 'news/confirm_delete.html', {'news': news})


@login_required
def edit_news(request, pk):
    """
    ویو برای ویرایش خبر (فقط توسط ادمین‌ها و سوپرکاربرها)
    """
    if request.user.user_type not in ['admin', 'superuser']:
        return render(request, 'news/error.html', {'error': 'Permission denied'})

    news = get_object_or_404(News, pk=pk)

    if request.method == 'POST':
        news.title = request.POST.get('title', news.title)
        news.summary = request.POST.get('summary', news.summary)
        news.content = request.POST.get('content', news.content)
        news.save()
        return redirect('news_detail', pk=news.id)

    return render(request, 'news/edit_news.html', {'news': news})
