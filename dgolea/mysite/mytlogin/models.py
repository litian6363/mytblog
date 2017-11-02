from django.db import models

from django.utils import timezone
# Create your models here.


class Users (models.Model):
    email = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    create_date = models.DateTimeField('create date', default=timezone.now())

    def __str__(self):
        return self.email

