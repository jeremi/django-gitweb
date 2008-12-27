from django import forms
from django.utils.translation import ugettext_lazy as _
from .models import Repository
import git

class RepositoryForm(forms.ModelForm):
    def clean_path(self):
        try:
            repo = git.Repo(self.cleaned_data['path'])
        except git.InvalidGitRepositoryError:
            raise forms.ValidationError(_('Please submit a valid git repository path'))
        except Exception:
            raise forms.ValidationError(_('Please submit a valid file path'))
        
        return self.cleaned_data['path']
        
    class Meta:
        model = Repository