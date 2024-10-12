from django import forms
from .models import DownloadVideo, ImageUpload


class YouTubeDownloadForm(forms.ModelForm):
    class Meta:
        model = DownloadVideo
        fields = ['youtube_url']


class ImageUploadForm(forms.ModelForm):
    class Meta:
        model = ImageUpload
        fields = ['image']