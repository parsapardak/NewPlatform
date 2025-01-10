from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views import View
from .models import Like
from news.models import News
from django.contrib import messages
from django.shortcuts import redirect


@method_decorator(login_required, name='dispatch')
class LikeNewsView(View):
    def post(self, request, news_id):
        news = get_object_or_404(News, pk=news_id)

        if Like.objects.filter(news=news, user=request.user).exists():
            messages.error(request, 'You have already liked this news.')
            return redirect('news_detail', pk=news_id)

        Like.objects.create(news=news, user=request.user)
        news.likes_count += 1
        news.save()

        messages.success(request, 'Thank you for liking the news!')
        return redirect('news_detail', pk=news_id)

@method_decorator(login_required, name='dispatch')
class UnlikeNewsView(View):
    def post(self, request, news_id):
        news = get_object_or_404(News, pk=news_id)

        like = Like.objects.filter(news=news, user=request.user).first()
        if not like:
            messages.error(request, 'You have not liked this news.')
            return redirect('news_detail', pk=news_id)

        like.delete()
        news.likes_count -= 1
        news.save()

        messages.success(request, 'You have successfully removed your like.')
        return redirect('news_detail', pk=news_id)
