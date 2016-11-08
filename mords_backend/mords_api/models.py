from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User


class Word(models.Model):
    text = models.CharField(max_length=200)

    def __unicode__(self):
        return self.text

    class Meta:
        ordering = ['text']


class Book(models.Model):
    name = models.CharField(max_length=200)
    word = models.ManyToManyField(Word, blank=True)

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['name']


class Learner(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE, blank=True)
    words_perDay = models.PositiveIntegerField(default=0)
    words_finished = models.PositiveIntegerField(default=0)

    def __unicode__(self):
        return self.user.username

    class Meta:
        ordering = ['user']


class Note(models.Model):
    word = models.ForeignKey(Word, related_name='word', on_delete=models.CASCADE)
    pub_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey('Learner', on_delete=models.CASCADE)
    text = models.TextField()

    def __unicode__(self):
        return self.text

    class Meta:
        ordering = ['word', 'text', 'author']





