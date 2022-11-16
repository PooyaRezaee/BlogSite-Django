from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    PROFILEINT = (
        (1, 'Man1'),
        (2, 'Man2'),
        (3, 'Woman1'),
        (4, 'Woman2'),
    )

    bio = models.TextField()
    avatar = models.IntegerField(default=1,choices=PROFILEINT)