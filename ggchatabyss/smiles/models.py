from django.db import models

# Create your models here.


class Smile(models.Model):
    gg_id = models.CharField(max_length=10)
    bind = models.CharField(max_length=20)
    name = models.CharField(max_length=100, unique=True)
    donat = models.IntegerField()
    premium = models.IntegerField()
    paid = models.IntegerField()
    animated = models.BooleanField()
    tag = models.CharField(max_length=100)
    img = models.CharField(max_length=255)
    img_big = models.CharField(max_length=255)
    img_gif = models.CharField(max_length=255)
    channel = models.CharField(max_length=255, null=True, blank=True)
    channel_id = models.CharField(max_length=32)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
