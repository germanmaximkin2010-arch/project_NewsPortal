from django.db import models
from django.contrib.auth.models import User


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)

    def update_rating(self):
        pr = sum(p.rating for p in Post.objects.filter(author=self)) * 3
        ur = sum(c.rating for c in Comment.objects.filter(user=self.user))
        cr = sum(c.rating for c in Comment.objects.filter(post__author=self))
        self.rating = pr + ur + cr
        self.save()


class Category(models.Model):
    category = models.CharField(max_length=100, unique=True)


class Post(models.Model):
    article = 'AR'
    news = 'NW'
    TYPE_CHOICES = ((article,'Статья'),(news,'Новости'))
    type = models.CharField(max_length=2, choices=TYPE_CHOICES, default=article)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    category = models.ManyToManyField(Category, through='PostCategory')
    title = models.CharField(max_length=255)
    content = models.TextField()
    rating = models.IntegerField(default = 0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self):
        if len(self.content) == 124:
            return self.content
        else:
            return self.content[0:123] + '...'


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text_comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default = 0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

