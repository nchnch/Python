#coding: utf-8
from django.conf.urls.defaults import patterns, include, url


urlpatterns = patterns('casino.views',
    url(r'^slots/$', 'slot_list'),
    url(r'^slots/(?P<item_id>\d+)/$', 'slot_page'),
)
