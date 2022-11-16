from django.db import models
from account.models import User
# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(User,on_delete=models.CASCADE)
    body = models.TextField()
    thumbnail = models.ImageField(upload_to='image_post')
    created = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.title