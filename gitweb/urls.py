from django.conf.urls.defaults import *

urlpatterns = patterns('',
    url(r'^$',
        'gitweb.views.repository_list',
        name='gitweb_repository_list'),
    url(r'^(?P<id>\d+)-(?P<slug>[\w-]+)/tree/(?P<branch>[\w-]+)/(?P<path>.*)$',
        'gitweb.views.repository_tree',
        name='gitweb_repository_tree'),
)