from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^(?P<word_text>[a-z]+)/$', views.detail, name='detail'),
    url(r'^(?P<word_text>[a-z]+)/note/$', views.note, name='note'),
    url(r'^(?P<word_text>[a-z]+)/know/$', views.know, name='know'),
    url(r'^latest_notes/$', views.latest_notes, name='latest_notes'),
]
