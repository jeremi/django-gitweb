from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
import os

class Repository(models.Model):
    path = models.FilePathField(_(u'Repository Path'))
    description = models.TextField(_(u'Description'), blank=True)
    is_public = models.BooleanField(_(u'Public Project'), default=False)
    members = models.ManyToManyField(Member)
    
    def __unicode__(self):
        return os.path.split(self.path)[-1]
    
    def get_absolute_url(self):
        pass # FIXME

class Member(models.Model):
    user = models.ForeignKey(User)
    can_download = models.BooleanField(default=True)
    can_view_content = models.BooleanField(default=True)
    
    def __unicode__(self):
        return self.user.username