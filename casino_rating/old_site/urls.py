#coding: utf-8
from django.conf.urls.defaults import patterns, include, url


urlpatterns = patterns('old_site.views',
    url(r'^(index.jsp)?$', 'index'),
    url(r'^casino_info.jsp$', 'casino'),
)
