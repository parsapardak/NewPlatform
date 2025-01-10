from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from .models import Comment
from news.models import News
from django.contrib.auth.decorators import login_required

@login_required
def add_comment(request, news_id):
    """
    ارسال نظر
    """
    news = get_object_or_404(News, pk=news_id)
    content = request.POST.get('content')

    if not content or len(content.strip()) == 0:
        messages.error(request, 'Comment content cannot be empty.')
        return redirect('news_detail', pk=news.id)

    if len(content) > 500:
        messages.error(request, 'Comment content is too long (max 500 characters).')
        return redirect('news_detail', pk=news.id)

    Comment.objects.create(
        news=news,
        user=request.user,
        content=content.strip()
    )
    messages.success(request, 'Your comment has been added.')
    return redirect('news_detail', pk=news.id)

@login_required
def add_reply(request, comment_id):
    """
    ارسال پاسخ به نظر
    """
    parent_comment = get_object_or_404(Comment, pk=comment_id)
    news = parent_comment.news
    content = request.POST.get('content')

    if not content or len(content.strip()) == 0:
        messages.error(request, 'Reply content cannot be empty.')
        return redirect('news_detail', pk=news.id)

    if len(content) > 500:
        messages.error(request, 'Reply content is too long (max 500 characters).')
        return redirect('news_detail', pk=news.id)

    Comment.objects.create(
        news=news,
        user=request.user,
        content=content.strip(),
        parent=parent_comment  # رابطه والد-فرزند
    )
    messages.success(request, 'Your reply has been added.')
    return redirect('news_detail', pk=news.id)
