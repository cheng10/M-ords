from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse


class Learner(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    username = User.username
    email = User.email
    vocab_book = models.ForeignKey('Book', on_delete=models.CASCADE, blank=True)
    words_perday = models.PositiveIntegerField(default=0)
    words_finished = models.PositiveIntegerField(default=0)

    def __unicode__(self):
        return self.user.username

    class Meta:
        ordering = ['user']


class Word(models.Model):
    text = models.CharField(max_length=200)

    def get_absolute_url(self):
        path = reverse('detail', kwargs={'id': self.id})
        return "localhost:8080%s" % path

    def __unicode__(self):
        return self.text

    class Meta:
        ordering = ['text']


class Book(models.Model):
    bookName = models.CharField(max_length=200)
    word = models.ManyToManyField('Word', blank=True)

    def __unicode__(self):
        return self.bookname

    class Meta:
        ordering = ['bookName']


class Note(models.Model):
    word = models.ForeignKey('Word', related_name='word', on_delete=models.CASCADE)
    author = models.ForeignKey('Learner', on_delete=models.CASCADE)
    text = models.TextField()

    def __unicode__(self):
        return self.text

    class Meta:
        ordering = ['word']





