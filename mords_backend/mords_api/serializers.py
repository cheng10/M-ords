from django.contrib.auth.models import User, Group
from rest_framework import serializers
from models import *


class UserSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='user-detail',
        lookup_field='username'
    )

    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'groups')


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'name')


class WordSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='word-detail',
        lookup_field='text'
    )

    class Meta:
        model = Word
        fields = ('url', 'text')


class BookSerializer(serializers.HyperlinkedModelSerializer):
    word = WordSerializer(many=True)
    url = serializers.HyperlinkedIdentityField(
        view_name='book-detail',
        lookup_field='name'
    )

    class Meta:
        model = Book
        fields = ('url', 'name', 'word')


class LearnerSerializer(serializers.HyperlinkedModelSerializer):
    # user = UserSerializer
    # book = BookSerializer
    user = serializers.StringRelatedField()
    book = serializers.StringRelatedField()
    # user = serializers.CharField(source='user.username')
    # url = serializers.HyperlinkedIdentityField(
    #     view_name='learner-detail',
    #     lookup_field='user'
    # )

    class Meta:
        model = Learner
        fields = ('url', 'user', 'book', 'words_perDay', 'words_finished')


class NoteSerializer(serializers.HyperlinkedModelSerializer):
    # word = WordSerializer
    word = serializers.StringRelatedField()
    author = LearnerSerializer

    class Meta:
        model = Note
        fields = ('url', 'word', 'pub_date', 'author', 'text')

