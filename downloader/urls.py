from django.urls import path
from .views import YouTubeAudioDownloadAPIView, ImageProcessAPIView


urlpatterns = [
    path('youtube/download/', YouTubeAudioDownloadAPIView.as_view(), name='youtube-download'),
    path('image/process/', ImageProcessAPIView.as_view(), name='image-process')
    # path('', views.download_youtube_audio, name='index'),
    # path('remove', views.upload_download_image, name='remove'),
]