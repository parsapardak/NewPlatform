from django.db import models
from accounts.models import CustomUser
from news.models import News


class Like(models.Model):
    news = models.ForeignKey(News, related_name='likes', on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Like by {self.user.username} on {self.news.title}"

    class Meta:
        unique_together = ('news', 'user')  # جلوگیری از ثبت لایک تکراری
