from django.conf import settings
from django.db import models
from django.utils import timezone

from blog.managers import PostPublishedManager, PostManager


# Create your models here.

class Post(models.Model):

    published = PostPublishedManager()

    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)
    is_published = models.BooleanField(default=False)

    objects = PostManager()
    published = PostPublishedManager()

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Запись в блоге'
        verbose_name_plural = 'Записи в блоге'

    def is_published(self):
        return True if self.published_date else False

class Comment(models.Model):
    post = models.ForeignKey('blog.Post', on_delete=models.CASCADE)
    author = models.CharField(max_length=200)
    text = models.TextField(verbose_name="Комментарий")
    created_date = models.DateTimeField(default=timezone.now())
    approved_comment = models.BooleanField(default=False)

    def approve(self):
        self.approved_comment = True
        self.save()

    def __str__(self):
        return self.text

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'