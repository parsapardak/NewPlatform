from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views import View
from .models import Comment
from news.models import News


@method_decorator(login_required, name='dispatch')
class CommentView(View):
    def post(self, request, news_id):
        """
        ارسال نظر برای خبر
        """
        news = get_object_or_404(News, pk=news_id)

        # فقط کاربران ثبت‌نام‌شده مجاز به ارسال نظر هستند
        if request.user.user_type != 'registered':
            return JsonResponse({'error': 'Only registered users can comment'}, status=403)

        content = request.POST.get('content')

        # بررسی محتوا
        if not content or len(content.strip()) == 0:
            return JsonResponse({'error': 'Comment content cannot be empty'}, status=400)
        if len(content) > 500:
            return JsonResponse({'error': 'Comment content is too long (max 500 characters)'}, status=400)

        # ایجاد نظر
        comment = Comment.objects.create(
            news=news,
            user=request.user,
            content=content.strip()
        )
        return JsonResponse({'message': 'Comment added successfully!', 'id': comment.id}, status=201)

    def delete(self, request, comment_id):
        """
        حذف نظر
        """
        comment = get_object_or_404(Comment, pk=comment_id)

        # فقط نویسنده یا ادمین‌ها می‌توانند نظر را حذف کنند
        if request.user != comment.user and request.user.user_type not in ['admin', 'superuser']:
            return JsonResponse({'error': 'Permission denied'}, status=403)

        # حذف نظر
        comment.delete()
        return JsonResponse({'message': 'Comment deleted successfully!'})
