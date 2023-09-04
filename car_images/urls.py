from django.urls import path
from .views import UploadFileView, ListAllFilesView


urlpatterns = [
    path('upload/', UploadFileView.as_view(),name='upload_image'),
    path('', ListAllFilesView.as_view(),name='list_images'),
]