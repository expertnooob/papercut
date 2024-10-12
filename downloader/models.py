from django.db import models


# Create your models here.
class DownloadVideo(models.Model):
    youtube_url = models.URLField()
    title = models.CharField(max_length=255)
    thumbnail_url = models.URLField()
    mp3_file = models.FileField(upload_to='mp3s/', blank=True, null=True)


class ImageUpload(models.Model):
    image = models.ImageField(upload_to='media/', blank=True, null=True)