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

