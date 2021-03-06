import settings
from django.conf.urls.defaults import patterns, include, url
from django.contrib import admin


admin.autodiscover()


urlpatterns = patterns('',
    #Home page url:
    url(r'^', include('old_site.urls')),

    #Modules URLs. 
    # url(r'^casino/', include('casino.casino_urls')),
    # url(r'^slots/', include('casino.game_urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)


if settings.DEBUG:
    urlpatterns += patterns('django.views.static',
        (r'^%s(?P<path>.*)$' % settings.MEDIA_URL.lstrip("/"), 'serve', {'document_root': settings.MEDIA_ROOT}),
    )

