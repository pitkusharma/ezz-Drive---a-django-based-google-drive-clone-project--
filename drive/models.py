from django.db import models
from django.contrib.auth.models import User


class Folder(models.Model):
    user = models.ForeignKey(
        User, 
        on_delete = models.CASCADE
        )
    parent_folder = models.IntegerField(
        null = True,
        blank = True
    )
    name = models.CharField(
        max_length = 50
    )
    def __str__(self) -> str:
        return self.name


def user_directory_path(instance, filename):
    return "user_{0}/{1}".format(instance.folder.user.id,filename) 

class File(models.Model):
    file = models.FileField(
        upload_to = user_directory_path
        )
    name = models.CharField(
        max_length = 100
    )
    size = models.IntegerField()
    date_of_upload = models.DateTimeField()
    folder = models.ForeignKey(
        Folder,
        on_delete = models.CASCADE
        )
    
    def __str__(self) -> str:
        return self.name    


