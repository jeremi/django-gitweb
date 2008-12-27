from django.template.context import RequestContext
from django.http import Http404
from django.shortcuts import render_to_response
import os

from gitweb.models import Repository

def repository_list(request, template_name='gitweb/repository_list.html'):
    template_context = {
        'repository_list': Repository.objects.visible_repositories_for_user(request.user),
    }
    
    return render_to_response(
        template_name,
        template_context,
        RequestContext(request)
    )

def repository_tree(request, id, slug, branch, path, template_name='gitweb/repository_tree.html'):
    try:
        repository = Repository.objects.visible_repositories_for_user(request.user).get(pk=id)
    except Repository.DoesNotExist:
        raise Http404

    tree = repository.repo().tree(branch)

    for element in path.split('/'):
        if len(element):
            tree = tree/element

    if hasattr(tree, 'mime_type'):
        is_blob = True
    else:
        is_blob = False
        tree = [{'path': os.path.join(path, e.name), 'e': e} for e in tree.values()]

    template_context = {
        'repository': repository,
        'branch': branch,
        'path': path,
        'prev_path': '/'.join(path.split('/')[0:-1]),
        'tree': tree,
        'is_blob': is_blob,
    }

    return render_to_response(
        template_name,
        template_context,
        RequestContext(request)
    )
