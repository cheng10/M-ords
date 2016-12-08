from django import forms
from mords_api.models import Learner
from django.contrib.auth.models import User


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password')


class LearnerForm(forms.ModelForm):
    class Meta:
        model = Learner
        fields = ('book', 'words_perDay', 'pic')
