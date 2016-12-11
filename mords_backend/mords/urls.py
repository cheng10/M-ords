from django.conf.urls import url
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'mords'
urlpatterns = [
    # url(r'^$', views.IndexView.as_view(), name='index'),
    # url(r'^new/$', views.NewView.as_view(), name='new'),
    url(r'^$', views.index, name='index'),
    url(r'^new/$', views.new, name='new'),
    url(r'^signup/$', views.signup, name='signup'),
    url(r'^logout/$', views.user_logout, name='logout'),
    url(r'^accounts/login/$', views.user_login, name='login'),
    url(r'^profile/$', views.update_profile, name='profile'),
    url(r'^update_password/$', views.update_password, name='password'),
    # url(r'^$', views.index, name='index'),
    # url(r'^(?P<word_text>[a-z]+)/$', views.DetailView.as_view, name='detail'),
    # url(r'^(?P<word_text>[a-z]+)/results/$', views.ResultsView.as_view, name='results'),
    url(r'^book/(?P<book_name>[a-zA-Z0-9\'\-\.\!_ ]+)/$', views.book_detail, name='book_detail'),
    url(r'^word/(?P<word_text>[a-zA-Z0-9\'\-\.\! ]+)/$', views.detail, name='detail'),
    url(r'^word/(?P<word_text>[a-zA-Z0-9\'\-\.\! ]+)/results/$', views.results, name='results'),
    url(r'^word/(?P<word_text>[a-zA-Z0-9\'\-\.\! ]+)/comment/$', views.comment, name='comment'),
    url(r'^word/(?P<word_text>[a-zA-Z0-9\'\-\.\! ]+)/note/$', views.note, name='note'),
    url(r'^word/(?P<word_text>[a-zA-Z0-9\'\-\.\! ]+)/know/$', views.know, name='know'),
    url(r'^latest_notes/$', views.latest_notes, name='latest_notes'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
