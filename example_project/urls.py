from django.conf.urls.defaults import *
from django.conf import settings
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^admin/(.*)', admin.site.root),
    (r'^', include('gitweb.urls')),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^media/django-gitweb/(?P<path>.*)$', 'django.views.static.serve', {'document_root': '../gitweb/media'}),
        (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    )