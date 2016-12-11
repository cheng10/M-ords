from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import datetime
from django.utils.encoding import python_2_unicode_compatible


@python_2_unicode_compatible
class Word(models.Model):
    text = models.CharField(max_length=200, unique=True)
    update_date = models.DateField(null=True)
    pron = models.CharField(max_length=200, default='',
                            help_text="pronunciation of the word")
    us_pho = models.CharField(max_length=200, default='')
    uk_pho = models.CharField(max_length=200, default='')
    is_info_get = models.BooleanField(default=False)

    def __str__(self):
        return self.text

    class Meta:
        ordering = ['text']


@python_2_unicode_compatible
class Book(models.Model):
    name = models.CharField(max_length=200)
    pub_date = models.DateField(null=True)
    update_date = models.DateField(null=True)
    desc = models.TextField(blank=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


@python_2_unicode_compatible
class Entry(models.Model):
    word = models.ForeignKey(Word, on_delete=models.CASCADE)
    defn = models.TextField(default='')
    exmp = models.TextField(default='')
    update_date = models.DateField(null=True)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)

    def __str__(self):
        return self.word.text

    class Meta:
        ordering = ['word']


@python_2_unicode_compatible
class Learner(models.Model):
    user = models.OneToOneField(User)
    book = models.ForeignKey(Book, on_delete=models.SET_NULL, blank=False, null=True)
    words_perDay = models.PositiveIntegerField(default=0)
    words_finished = models.PositiveIntegerField(default=0)
    pic = models.ImageField(upload_to='profile_images', blank=True)

    def __str__(self):
        return self.user.username

    class Meta:
        ordering = ['user']


@python_2_unicode_compatible
class Note(models.Model):
    word = models.ForeignKey(Word, on_delete=models.CASCADE)
    pub_date = models.DateTimeField(blank=False)
    author = models.ForeignKey(Learner, on_delete=models.CASCADE)
    text = models.TextField()

    def __str__(self):
        return self.text

    class Meta:
        ordering = ['word', 'text', 'author']

    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now




