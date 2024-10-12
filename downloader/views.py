import os
import base64
import logging

import tempfile

from django.shortcuts import render
from django.http import HttpResponse

from pytube import YouTube
from rembg import remove

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .forms import YouTubeDownloadForm, ImageUploadForm
from .serializers import VideoSerializer, ImageSerializer


# --------------------------DRFViews -------------------------

class YouTubeAudioDownloadAPIView(APIView):
    def post(self, request):
        serializer = VideoSerializer(data=request.data)
        if serializer.is_valid():
            try:
                video_url = serializer.validated_data['youtube_url']
                yt = YouTube(video_url)
                title = yt.title
                thumbnail_url = yt.thumbnail_url

                if 'download' in request.data:
                    if request.data['download'] == 'true':
                        stream = yt.streams.filter(only_audio=True).first()

                        with tempfile.NamedTemporaryFile(suffix='.mp3', delete=False) as temp_audio:
                            stream.download(output_path=temp_audio.name[:temp_audio.name.rfind(os.path.sep)])
                            temp_audio_path = temp_audio.name

                        with open(temp_audio_path, 'rb') as file:
                            audio_data = file.read()

                        os.unlink(temp_audio_path)

                        response = Response(audio_data, content_type='audio/mpeg')
                        response['Content-Disposition'] = f'attachment; filename="{title}.mp3"'
                        return response
                    else:
                        return Response({"title": title, "thumbnail_url": thumbnail_url})
                else:
                    return Response({"title": title, "thumbnail_url": thumbnail_url})
            except Exception as e:
                return Response({"detail": f"An error occurred: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ImageProcessAPIView(APIView):
    def post(self, request):
        serializer = ImageSerializer(data=request.data)
        if serializer.is_valid():
            try:
                image_file = serializer.validated_data.get('image')
                if image_file:
                    image_bytes = image_file.read()
                    processed_image_bytes = remove(image_bytes)

                    if 'download' in request.data:
                        response = HttpResponse(processed_image_bytes, content_type='image/png')
                        response['Content-Disposition'] = 'attachment; filename="processed_image.png"'
                        return response
                    else:
                        processed_image_base64 = base64.b64encode(processed_image_bytes).decode('utf-8')
                        return Response({"processed_image": processed_image_base64}, status=status.HTTP_200_OK)
                else:
                    return Response({"detail": "Image not found"}, status=status.HTTP_400_BAD_REQUEST)
            except Exception as e:
                return Response({"detail": f"An error occurred: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# -------------------------- Views ---------------------------
# def download_youtube_audio(request):
#     title = ''
#     thumbnail_url = ''
#     error_message = None
#     form = YouTubeDownloadForm()
#
#     if request.method == 'POST':
#         form = YouTubeDownloadForm(request.POST)
#         if form.is_valid():
#             try:
#                 video_url = form.cleaned_data['youtube_url']
#                 yt = YouTube(video_url)
#                 title = yt.title
#                 thumbnail_url = yt.thumbnail_url
#
#                 if 'download' in request.POST:
#                     stream = yt.streams.filter(only_audio=True).first()
#
#                     with tempfile.NamedTemporaryFile(suffix='.mp3', delete=False) as temp_audio:
#                         stream.download(output_path=temp_audio.name[:temp_audio.name.rfind(os.path.sep)])
#                         temp_audio_path = temp_audio.name
#
#                     with open(temp_audio_path, 'rb') as file:
#                         response = HttpResponse(file.read(), content_type='audio/mpeg')
#                         response['Content-Disposition'] = f'attachment; filename="{title}.mp3"'
#                         return response
#                 else:
#                     error_message = f"Unable to Download"
#             except Exception as e:
#                 error_message = f"An error occurred: {e}"
#         else:
#             error_message = "Please enter a valid YouTube URL."
#
#     context = {'form': form,
#                'title': title,
#                'thumbnail_url': thumbnail_url,
#                'error_message': error_message}
#     return render(request, 'downloader/download.html', context)
#
#
# def upload_download_image(request):
#     processed_image = None
#     error_message = ''
#
#     if request.method == 'POST':
#         image_form = ImageUploadForm(request.POST, request.FILES)
#         if image_form.is_valid():
#             image_file = request.FILES.get('image')
#             if image_file:
#                 image_bytes = image_file.read()
#                 processed_image_bytes = remove(image_bytes)
#                 processed_image = base64.b64encode(processed_image_bytes).decode('utf-8')
#             else:
#                 error_message = "Image not found"
#
#         if 'download_src' in request.POST:
#             image_data = base64.b64decode(request.POST["download_src"])
#             response = HttpResponse(image_data, content_type='image/png')
#             response['Content-Disposition'] = f'attachment; filename="processed_image.png"'
#             return response
#     else:
#         image_form = ImageUploadForm()
#
#     context = {'image_form': image_form, 'processed_image': processed_image, 'error_message': error_message}
#
#     return render(request, 'downloader/remove_bg.html', context)
