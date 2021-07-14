from django.contrib.auth.models import User
from django.db import models


class Post(models.Model):
    title = models.CharField('Заголовок', max_length=256, unique=True)
    creator = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_on = models.DateTimeField(auto_now_add=True)
    url = models.URLField('Ссылка', max_length=256, blank=True)
    votes = models.IntegerField(null=True, default=0)
    comments = models.IntegerField(null=True, default=0)

    def __str__(self):
        return self.title

    def count_votes(self):
        self.votes = Vote.objects.filter(post=self).count()

    def count_comments(self):
        self.comments = Comment.objects.filter(post=self).count()


class Vote(models.Model):
    voter = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user.username} лайкнул {self.link.title}'


class Comment(models.Model):
    creator = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    content = models.TextField()
    identifier = models.IntegerField()
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f'{self.user.username} прокомментировал(-a)'
