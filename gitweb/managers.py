from django.db import models
from django.db.models import Q

REPOSITORY_PUBLIC_FILTER = lambda u: Q(is_public=True)
REPOSITORY_LOGGED_IN_FILTER = lambda u: Q(Q(is_public=True) | Q(member__user=u))

class RepositoryManager(models.Manager):
    def visible_repositories_for_user(self, user=None):
        if not user or not user.is_authenticated():
            qset = REPOSITORY_PUBLIC_FILTER(user)
        else:
            qset = REPOSITORY_LOGGED_IN_FILTER(user)
        
        return self.get_query_set().filter(qset)