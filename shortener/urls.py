# -*- coding: utf-8 -*-

from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^(?P<url_id>[A-Za-z]{8})$', views.reverse, name='reverse'),
]
