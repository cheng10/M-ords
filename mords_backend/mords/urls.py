from django.conf.urls import url
from . import views

app_name = 'mords'
urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^signup/$', views.signup, name='signup'),
    url(r'^logout/$', views.user_logout, name='logout'),
    url(r'^accounts/login/$', views.user_login, name='login'),
    # url(r'^$', views.index, name='index'),
    # url(r'^(?P<word_text>[a-z]+)/$', views.DetailView.as_view, name='detail'),
    # url(r'^(?P<word_text>[a-z]+)/results/$', views.ResultsView.as_view, name='results'),
    url(r'^word/(?P<word_text>[a-z]+)/$', views.detail, name='detail'),
    url(r'^word/(?P<word_text>[a-z]+)/results/$', views.results, name='results'),
    url(r'^word/(?P<word_text>[a-z]+)/comment/$', views.comment, name='comment'),
    url(r'^word/(?P<word_text>[a-z]+)/note/$', views.note, name='note'),
    url(r'^word/(?P<word_text>[a-z]+)/know/$', views.know, name='know'),
    url(r'^latest_notes/$', views.latest_notes, name='latest_notes'),
]
