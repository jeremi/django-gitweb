import logging
import os

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.conf import settings
from django.db.models import Q
import git

# we show only the public repository to the public users
REPOSITORY_PUBLIC_FILTER = lambda u: Q(Q(is_public=True) & Q(is_enabled=True))

#we show to the login users :
# * the public repos
# * the repository with no members assigned
# * the repository where he is member
REPOSITORY_LOGGED_IN_FILTER = lambda u: Q(Q(Q(is_public=True)|Q(member__user=None)| Q(member__user=u)) & Q(is_enabled=True))

class RepositoryManager(models.Manager):
    def visible_repositories_for_user(self, user=None):
        if not user or not user.is_authenticated():
            qset = REPOSITORY_PUBLIC_FILTER(user)
        else:
            qset = REPOSITORY_LOGGED_IN_FILTER(user)
        
        return self.get_query_set().filter(qset)
    
    def sync_with_fs(self):
        result = { 'created':[], 'errors':[], 'outdated':[] }

        entries = os.listdir(settings.GIT_REPOSITORY)
        repositories = Repository.objects.values_list('path', flat=True).order_by('id')

        # In the filesystem but not in the database, should either create or update
        for entrie in entries:
            repository_path = os.path.join(settings.GIT_REPOSITORY, entrie)
            if not os.path.isdir(repository_path): continue
            try:
                #if there is no .git directory, so it's not a git repository
                # so we simply skip it
                if not os.path.isdir(os.path.join(repository_path, '.git')): continue
                
                defaults = dict(
                    title = entrie,
                    path = repository_path,
                )
                respository, created = Repository.objects.get_or_create(path = repository_path, defaults=defaults)
                
                if created:
                    logging.debug("the repository '%s' is added" % entrie)
                    result['created'].append(entrie)
                    
            except Exception:
                logging.exception("Couldn't load repository '%s' from the filesystem" % entrie)
                result['errors'].append(entrie)

        # In the database but not on the filesystem, we log it
        for repo_path in [ repo_path for repo_path in repositories if not os.path.isdir(os.path.join(repo_path, '.git')) ]:
            respository = Repository.objects.get(path=repo_path)
            result['outdated'].append(entrie)
            logging.warning("the repository '%s' is not available on the filesystem" % respository.title)
            respository.delete()

        return result

class Repository(models.Model):
    path = models.CharField(_('Repository Path'), max_length=255)
    title = models.CharField(_('Title'), max_length=255)
    slug = models.SlugField(_('Slug'), max_length=255, blank=True)
    description = models.TextField(_('Description'), blank=True)
    is_public = models.BooleanField(_('Is Public'), default=False)
    is_enabled = models.BooleanField(_('Is Enabled'), default=True)
    
    objects = RepositoryManager()
    
    def slugify_uniquely(self, value, slugfield="slug"):
        from django.template.defaultfilters import slugify
        suffix = 0
        potential = base = slugify(value)
        while True:
            if suffix:
                potential = "-".join([base, str(suffix)])
            if not self.__class__.objects.filter(**{slugfield: potential}).count():
                return potential
            # we hit a conflicting slug, so bump the suffix & try again
            suffix += 1

    
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self.slugify_uniquely(self.title)
        super(Repository, self).save(*args, **kwargs)
        
    def __unicode__(self):
        return self.title
    
    def get_absolute_tree_url(self):
        return reverse(viewname='gitweb.views.repository_summary',
                       kwargs={'slug': self.slug})
    
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
