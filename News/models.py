from django.db import models
from django.db.models import *
from django.contrib.auth.models import User, Group
from django.core.validators import MinValueValidator


class Author (models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rating_author = models.IntegerField(default=0)

    class Meta:
        verbose_name = 'Автор'
        verbose_name_plural = 'Авторы'

    def update_rating(self):
        post_sum = Post.objects.filter(author=self).aggregate(s_post=Sum('rating_post'))
        comm_author_sum = Comment.objects.filter(user=self).aggregate(s1_comm=Sum('rating_comment'))
        comm_post_sum = Comment.objects.filter(post__author=self).aggregate(s2_comm=Sum('rating_comment'))
        self.rating_author = post_sum['s_post'] * 3 + comm_author_sum['s1_comm'] + comm_post_sum['s2_comm']
        self.save()


class Category(models.Model):
    name = models.TextField(unique=True)
    subscribers = models.ManyToManyField(User, through='CategorySubscribers')

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return f'{self.name}'


class CategorySubscribers(models.Model):
    sub_categories = models.ForeignKey(Category, on_delete=models.CASCADE)
    sub_user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.sub_categories}, {self.sub_users}'


class Post (models.Model):
    ARTICLE = 'AR'
    NEWS = 'NW'

    TYPES = [
        (ARTICLE, 'Статья'),
        (NEWS, 'новость'),
    ]
    ar_or_nw = models.CharField(max_length=2, choices=TYPES, default=NEWS)
    publish = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=255)
    body = models.TextField()
    rating_post = models.IntegerField(default=0)

    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    category = models.ManyToManyField(Category, through='PostCategory')

    class Meta:
        verbose_name = 'Публикация'
        verbose_name_plural = 'Публикации'

    def preview(self):
        return f'Заголовок: {self.title}\n Статья: {self.text[:124]} ...'

    def get_categories(self):
        result = []
        for category in self.category.all():
            result.append(category)
        return result

    def like(self):
        self.rating_post += 1
        self.save()

    def dislike(self):
        self.rating_post -= 1
        self.save()


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    comment_text = models.TextField()
    publish_comment = models.DateTimeField(auto_now_add=True)
    rating_comment = models.IntegerField(default=0)

    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(Author, on_delete=models.CASCADE)

    def like(self):
        self.rating_comment += 1
        self.save()

    def dislike(self):
        self.rating_comment -= 1
        self.save()
