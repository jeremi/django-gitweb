from gitweb.models import Repository
from django.shortcuts import render_to_response
from django.template.context import RequestContext

def repository_list(request, template_name='gitweb/repository_list.html'):
    template_context = {'repository_list': Repository.objects.all(),}
    return render_to_response(template_name, template_context,
                              RequestContext(request))
    
def gitweb_repository_tree(request, project_name, hash_name):
    pass

def gitweb_repository_commits(request, project_name, hash_name):
    pass