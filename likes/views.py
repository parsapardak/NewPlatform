from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views import View
from .models import Like
from news.models import News

@method_decorator(login_required, name='dispatch')
class LikeView(View):
    def post(self, request, news_id):
        news = get_object_or_404(News, pk=news_id)

        # Check if the user already liked the news
        if Like.objects.filter(news=news, user=request.user).exists():
            return JsonResponse({'error': 'You have already liked this news'}, status=400)

        Like.objects.create(news=news, user=request.user)
        news.likes_count += 1
        news.save()

        return JsonResponse({'message': 'News liked successfully!'})

    def delete(self, request, news_id):
        news = get_object_or_404(News, pk=news_id)
        like = Like.objects.filter(news=news, user=request.user).first()

        if not like:
            return JsonResponse({'error': 'You have not liked this news'}, status=400)

        like.delete()
        news.likes_count -= 1
        news.save()

        return JsonResponse({'message': 'Like removed successfully!'})
