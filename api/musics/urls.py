from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^list', views.MusicViewSet.all_singer,
        name='all_singer')]