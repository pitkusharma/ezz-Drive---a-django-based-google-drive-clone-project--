from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
        ('others', 'Others')
    ]
    gender = models.CharField(max_length=6, default='male', choices=GENDER_CHOICES)


    def __str__(self):
        return self.user.first_name