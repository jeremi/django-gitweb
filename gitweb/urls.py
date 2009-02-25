from django.conf.urls.defaults import *

urlpatterns = patterns('',
    url(r'^$',
        'gitweb.views.repository_list',
        name='gitweb_repository_list'),
    url(r'^(?P<slug>[\w-]+)/$',
        'gitweb.views.repository_summary',
        name='gitweb_repository_summary'),
    url(r'^(?P<slug>[\w-]+)/commit/(?P<commit>[\w-]+)/$',
        'gitweb.views.repository_commit',
        name='gitweb_repository_commit'),
    url(r'^(?P<slug>[\w-]+)/commit/(?P<commit>[\w-]+)/diff/$',
        'gitweb.views.repository_commit', {'template_name': 'gitweb/repository_commit_diff.html'},
        name='gitweb_repository_commit_diff'),
    url(r'^(?P<slug>[\w-]+)/tree/(?P<branch>[\w-]+)/(?P<path>.*)$',
        'gitweb.views.repository_tree',
        name='gitweb_repository_tree'),
)