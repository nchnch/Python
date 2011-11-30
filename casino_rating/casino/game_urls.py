#coding: utf-8
from django.conf.urls.defaults import patterns, include, url


urlpatterns = patterns('casino.views',
    url(r'^$', 'game_list'),
    url(r'^(?P<item_id>\d+)/$', 'game_page'),
)
