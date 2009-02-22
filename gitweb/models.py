from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.conf import settings
from django.template.defaultfilters import slugify
import os
import git
from .managers import RepositoryManager

class Repository(models.Model):
    path = models.CharField(_('Repository Path'), max_length=255)
    title = models.CharField(_('Title'), max_length=255)
    slug = models.SlugField(_('Slug'), max_length=255, blank=True)
    description = models.TextField(_('Description'), blank=True)
    is_public = models.BooleanField(_('Is Public'), default=False)
    
    objects = RepositoryManager()
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(os.path.split(self.path)[-1])
        super(Repository, self).save(*args, **kwargs)
        
    def __unicode__(self):
        return self.title
    
    def get_absolute_tree_url(self):
        return reverse(viewname='gitweb_repository_tree',
                       kwargs={'id': self.pk,
                               'slug': self.slug,
                               'branch': self.active_branch})
    
    """
    def get_absolute_commits_url(self):
        return reverse(viewname='gitweb_repository_commits',
                       kwargs={'project_name': self.slug,
                               'hash_name': self.active_branch()})
    """
    
    def get_absolute_url(self):
        return self.get_absolute_tree_url()
    
    def repo(self):
        return git.Repo(self.path)
    
    def branches(self):
        branches = self.repo().branches
        return branches
    
    @property
    def active_branch(self):
        return self.repo().active_branch
    
    @property
    def tags(self):
        return self.repo().tags
    
    @property
    def recent_commits(self):
        return self.repo().commits(max_count=getattr(settings, 'GITHUB_RECENT_COMMITS_COUNT', 10))
    
    @property
    def last_commit(self):
        return self.repo().commits(max_count=1)[0]
    
    class Meta:
        verbose_name = _('Repository')
        verbose_name_plural = _('Repositories')

class Member(models.Model):
    repository = models.ForeignKey(Repository, verbose_name=_('Repository'))
    user = models.ForeignKey(User, verbose_name=_('User'))
    can_download = models.BooleanField(_('Can download'), default=True)
    can_view_content = models.BooleanField(_('Can view content'), default=True)
    
    def __unicode__(self):
        return '%s: %s' % (self.repository, self.user)
    
    class Meta:
        unique_together = ('repository', 'user')
        verbose_name = _('Repository User')
        verbose_name_plural = _('Repository Users')
