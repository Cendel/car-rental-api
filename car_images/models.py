from django.db import models


# Create your models here.

class Image(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)
    image = models.ImageField(upload_to='images/')
    size = models.IntegerField(default=1024, blank=True, null=True)
    type = models.CharField(max_length=100, blank=True, null=True)
