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
        """
        لایک کردن یک خبر
        """
        # فقط کاربران registered مجاز به لایک هستند
        if request.user.user_type != 'registered':
            return JsonResponse({'error': 'Permission denied'}, status=403)

        news = get_object_or_404(News, pk=news_id)

        # بررسی اینکه کاربر قبلاً این خبر را لایک نکرده باشد
        if Like.objects.filter(news=news, user=request.user).exists():
            return JsonResponse({'error': 'You have already liked this news'}, status=400)

        # ایجاد لایک
        Like.objects.create(news=news, user=request.user)
        return JsonResponse({'message': 'News liked successfully!'})

    def delete(self, request, news_id):
        """
        حذف لایک از یک خبر
        """
        news = get_object_or_404(News, pk=news_id)

        # یافتن لایک کاربر
        like = Like.objects.filter(news=news, user=request.user).first()

        if not like:
            return JsonResponse({'error': 'You have not liked this news'}, status=400)

        # حذف لایک
        like.delete()
        return JsonResponse({'message': 'Like removed successfully!'})
