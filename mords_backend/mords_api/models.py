from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import datetime
from django.utils.encoding import python_2_unicode_compatible


@python_2_unicode_compatible
class Word(models.Model):
    text = models.CharField(max_length=200)

    def __str__(self):
        return self.text

    class Meta:
        ordering = ['text']


@python_2_unicode_compatible
class Book(models.Model):
    name = models.CharField(max_length=200)
    word = models.ManyToManyField(Word, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


@python_2_unicode_compatible
class Learner(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE, blank=True)
    words_perDay = models.PositiveIntegerField(default=0)
    words_finished = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.user.username

    class Meta:
        ordering = ['user']


@python_2_unicode_compatible
class Note(models.Model):
    word = models.ForeignKey(Word, on_delete=models.CASCADE)
    pub_date = models.DateTimeField()
    author = models.ForeignKey('Learner', on_delete=models.CASCADE)
    text = models.TextField()

    def __str__(self):
        return self.text

    class Meta:
        ordering = ['word', 'text', 'author']

    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now




