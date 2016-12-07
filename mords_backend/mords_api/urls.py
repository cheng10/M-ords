from django.conf.urls import url, include
from . import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)
router.register(r'learner', views.LearnerViewSet)
router.register(r'book', views.BookViewSet)
router.register(r'word', views.WordViewSet)
router.register(r'note', views.NoteViewSet)

urlpatterns = [
    url(r'^', include(router.urls), name='api')
]
