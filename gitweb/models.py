from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
import os
import git

class Member(models.Model):
    user = models.ForeignKey(User)
    can_download = models.BooleanField(default=True)
    can_view_content = models.BooleanField(default=True)
    
    def __unicode__(self):
        return self.user.username

class Repository(models.Model):
    path = models.CharField(_(u'Repository Path'), max_length=255)
    title = models.CharField(_(u'Title'), max_length=255)
    slug = models.SlugField(_(u'SlugField'), max_length=255, blank=True)
    description = models.TextField(_(u'Description'), blank=True)
    is_public = models.BooleanField(_(u'Public Project'), default=False)
    members = models.ManyToManyField(Member, blank=True, null=True)
    
    def save(self, *args, **kwargs):
        if not self.pk:
            self.slug = os.path.split(self.path)[-1]
            if not self.title:
                self.title = self.slug
        super(Repository, self).save(*args, **kwargs)
        
    def __unicode__(self):
        return self.slug
    
    def get_absolute_tree_url(self):
        return reverse(viewname='gitweb_repository_tree',
                       kwargs={'project_name': self.slug,
                               'hash_name': self.active_branch()})
    
    def get_absolute_commits_url(self):
        return reverse(viewname='gitweb_repository_commits',
                       kwargs={'project_name': self.slug,
                               'hash_name': self.active_branch()})
    
    def get_absolute_url(self):
        return self.get_absolute_tree_url()

    def repo(self):
        return git.Repo(self.path)
    
    def branches(self):
        branches = self.repo().branches
        return branches
    
    def active_branch(self):
        return self.repo().active_branch

    def tags(self):
        return self.repo().tags
    
    def recent_commits(self):
        commits = self.repo().commits(max_count=3)
        print dir(commits[0])
        return commits