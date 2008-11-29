from django.conf.urls.defaults import *

urlpatterns = patterns('',
    url(r'^$', 'gitweb.views.repository_list', name='gitweb_repository_list'),
    url(r'^(?P<project_name>[\w\-]+)/tree/(?P<hash>[\w\-]+)/$',
        'gitweb.views.repository_tree', name='gitweb_repository_tree'),
    url(r'^(?P<project_name>[\w\-]+)/commits/(?P<hash>[\w\-]+)/$',
        'gitweb.views.repository_tree', name='gitweb_repository_commits'),
)