from django.db import models
from django.db.models import *
from django.contrib.auth.models import User


class Author (models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rating_author = models.IntegerField(default=0)

    def update_rating(self):
        post_sum = Post.objects.filter(author=self).aggregate(s_post=Sum('rating_post'))
        comm_author_sum = Comment.objects.filter(user=self).aggregate(s1_comm=Sum('rating_comment'))
        comm_post_sum = Comment.objects.filter(post__author=self).aggregate(s2_comm=Sum('rating_comment'))
        self.rating_author = post_sum['s_post'] * 3 + comm_author_sum['s1_comm'] + comm_post_sum['s2_comm']
        self.save()


class Category(models.Model):
    name = models.TextField(unique=True)


class Post (models.Model):
    T_CHOICES = (
    ('AR', 'Статья'),
    ('NW', 'Новость'),
    )
    ar_or_nw = models.CharField(max_length=2, choices=T_CHOICES, default='AR')
    publish = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=255)
    body = models.TextField()
    rating_post = models.IntegerField(default=0)

    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    category = models.ManyToManyField(Category, through='PostCategory')

    def preview(self):
        len_ = 124 if len(self.body) > 124 else len(self.body)
        return self.body[:len_]+'...'

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