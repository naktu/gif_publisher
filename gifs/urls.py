from django.conf.urls import url
from gifs import views


urlpatterns = [
    url(r'^gifs/$', views.gifs_list)
]
