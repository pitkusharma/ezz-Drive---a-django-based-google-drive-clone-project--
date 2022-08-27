from django.db import models
# from django.contrib.auth.models import User
from user.models import UserProfile


class Folder(models.Model):
    user = models.ForeignKey(
        UserProfile, 
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


class File(models.Model):
    folder = models.ForeignKey(
        Folder,
        on_delete = models.CASCADE
    )
    name = models.CharField(
        max_length = 100
    )
    date_of_upload = models.DateTimeField()
    size = models.IntegerField()
    file = models.FileField()
    def __str__(self) -> str:
        return self.name    


# Create your models here.
