from django.urls import path
from .views import UploadFileView, ListAllFilesView, download_file, display_image, delete_file


urlpatterns = [
    path('upload/', UploadFileView.as_view(),name='upload_image'),
    path('', ListAllFilesView.as_view(),name='list_images'),
    path('download/<int:image_id>/', download_file, name='image_download'),
    path('display/<int:image_id>/', display_image, name='image_show'),
    path('<int:image_id>/', delete_file, name='image_delete'),
]

