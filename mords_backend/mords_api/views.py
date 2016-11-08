from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAdminUser, AllowAny, IsAuthenticated

from serializers import *


@permission_classes((IsAdminUser, ))
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    lookup_field = 'username'


@permission_classes((IsAdminUser, ))
class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


@permission_classes((AllowAny, ))
class WordViewSet(viewsets.ModelViewSet):
    queryset = Word.objects.all()
    serializer_class = WordSerializer
    lookup_field = 'text'


@permission_classes((AllowAny, ))
class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    lookup_field = 'name'


@permission_classes((IsAuthenticated, ))
class LearnerViewSet(viewsets.ModelViewSet):
    # user = serializers.CharField(source='user.username')
    queryset = Learner.objects.all()
    serializer_class = LearnerSerializer
    # lookup_field = 'user'

    # def get_queryset(self):
    #     username = str(self.kwargs["user"])
    #     user = User.objects.get(username=username)
    #     return Learner.objects.filter(user=user)


@permission_classes((AllowAny, ))
class NoteViewSet(viewsets.ModelViewSet):
    queryset = Note.objects.all()
    serializer_class = NoteSerializer
