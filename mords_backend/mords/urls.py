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
    url(r'^learn/$', views.learn, name='learn'),
    url(r'^review/$', views.review, name='review'),
    url(r'^learn_res/(?P<word_id>[0-9]+)/$', views.learn_res, name='learn_res'),
    url(r'^cross_res/(?P<word_id>[0-9]+)/$', views.cross_res, name='cross_res'),
    url(r'^search/$', views.search, name='search'),
    url(r'^signup/$', views.signup, name='signup'),
    url(r'^logout/$', views.user_logout, name='logout'),
    url(r'^accounts/login/$', views.user_login, name='login'),
    url(r'^profile/$', views.update_profile, name='profile'),
    url(r'^update_password/$', views.update_password, name='password'),
    # url(r'^$', views.index, name='index'),
    # url(r'^(?P<word_text>[a-z]+)/$', views.DetailView.as_view, name='detail'),
    # url(r'^(?P<word_text>[a-z]+)/results/$', views.ResultsView.as_view, name='results'),
    url(r'^book/(?P<book_name>[a-zA-Z0-9\'\-\.\!_ ]+)/$', views.book_detail, name='book_detail'),
    url(r'^word/(?P<word_id>[0-9]+)/$', views.detail, name='detail'),
    url(r'^results/(?P<word_id>[0-9]+)/$', views.results, name='results'),
    url(r'^comment/(?P<word_id>[0-9]+)/$', views.comment, name='comment'),
    url(r'^tick/(?P<word_id>[0-9]+)/$', views.tick, name='tick'),
    url(r'^cross/(?P<word_id>[0-9]+)/$', views.cross, name='cross'),
    url(r'^cross2/(?P<word_id>[0-9]+)/$', views.cross2, name='cross2'),
    url(r'^latest_notes/$', views.latest_notes, name='latest_notes'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
