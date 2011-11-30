#coding: utf-8
from django.conf.urls.defaults import patterns, include, url


urlpatterns = patterns('casino.views',
    url(r'^$', 'casino_list'),
    url(r'^(?P<item_id>\d+)/$', 'casino_page'),
)
