import settings
from django.conf.urls.defaults import patterns, include, url
from django.contrib import admin


admin.autodiscover()


urlpatterns = patterns('',
    #Home page url:
    url(r'^$', 'casino_rating.views.home'),

    #Modules URLs. 
    url(r'^casino/', include('casino.casino_urls')),
    url(r'^slots/', include('casino.game_urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)


if settings.DEBUG:
    urlpatterns += patterns('django.views.static',
        (r'^%s(?P<path>.*)$' % settings.MEDIA_URL.lstrip("/"), 'serve', {'document_root': settings.MEDIA_ROOT}),
    )

