from django.urls import path
from .views import SampleAPIView, SweAPIView, FileUploadView

urlpatterns = [
    path('test/', SampleAPIView.as_view(), name='test'),
    path('api/swe_eval/', SweAPIView.as_view(), name='swe_eval'),
    path('api/file_upload/', FileUploadView.as_view(), name='file_upload'),,
]