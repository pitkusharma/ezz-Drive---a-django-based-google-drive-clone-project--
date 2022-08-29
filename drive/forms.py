from email.policy import default
from random import choices
from django import forms
from .models import Folder

class FolderForm(forms.Form):
    name = forms.CharField(
        max_length = 50,
        label = ""
    )


class FileForm(forms.Form):
    file = forms.FileField(
        label = "Upload File"
    )


class SetParameterForm(forms.Form):
    choices = [
        ('date', 'Date'),
        ('name', 'Name'),
        ('size', 'Size')        
    ]
    order = forms.ChoiceField(choices = choices)
    reverse = forms.BooleanField(required = False)


class RenameForm(forms.Form):
    name = forms.CharField(
        max_length = 50,
        label = ""
    )