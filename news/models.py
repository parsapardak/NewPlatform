from django.db import models
from accounts.models import CustomUser


class News(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    published_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    class Meta:
        ordering = ['-published_date']  # مرتب‌سازی پیش‌فرض نزولی بر اساس تاریخ انتشار

    @property
    def likes_count(self):
        return self.likes.count()  # شمارش خودکار تعداد لایک‌ها

    @property
    def comments_count(self):
        return self.comments.count()  # شمارش خودکار تعداد نظرات

    def __str__(self):
        return self.title
