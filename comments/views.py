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
        news = get_object_or_404(News, pk=news_id)
        content = request.POST.get('content')

        if not content:
            return JsonResponse({'error': 'Comment content is required'}, status=400)

        comment = Comment.objects.create(
            news=news,
            user=request.user,
            content=content
        )
        return JsonResponse({'message': 'Comment added successfully!', 'id': comment.id}, status=201)

    def delete(self, request, comment_id):
        comment = get_object_or_404(Comment, pk=comment_id, user=request.user)
        comment.delete()
        return JsonResponse({'message': 'Comment deleted successfully!'})
