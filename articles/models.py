from django.db import models
from django.contrib.auth.models import User, Permission
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth import get_user_model

class Author(models.Model):
    first_name = models.CharField(max_length=50, null=False, blank=False)
    last_name = models.CharField(max_length=50, null=False, blank=False)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class Article(models.Model):
    title = models.CharField(max_length=200, null=False, blank=False)
    author = models.ForeignKey(
        get_user_model(),
        on_delete = models.SET_DEFAULT,
        default = 1,
        related_name = 'article'
    )
    body = models.TextField(max_length=3000, null=False, blank=False)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    tags = models.ManyToManyField(
        'articles.Tag',
        related_name = 'articles',
        blank = True
    )

    def __str__(self):
        return f'{self.pk}.{self.title}'

    class Meta:
        verbose_name = 'Article'
        verbose_name_plural = 'Articles'
        permissions = [
            ('can_read_article', '有权限读文章')
        ]

    @classmethod
    def create_permissions(cls):
        content_type = ContentType.objects.get_for_model(cls)
        Permission.objects.get_or_create(
            codename='view_article',
            name='Can view article',
            content_type=content_type,
        )

class Comment(models.Model):
    article = models.ForeignKey('articles.Article', on_delete=models.CASCADE, related_name='comments')
    text = models.TextField(max_length=500)
    author = models.ForeignKey(
        get_user_model(),
        on_delete = models.SET_DEFAULT,
        default = 1,
        related_name = 'comment'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.text[:20]

class Tag(models.Model):
    name = models.CharField(max_length=30, verbose_name='Tag')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name