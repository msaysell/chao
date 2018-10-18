from django.conf.urls import url
from Dashboard import views

__author__ = 'Michael'


urlpatterns = [url(r'^home', views.index, name='admin_home'), ]
