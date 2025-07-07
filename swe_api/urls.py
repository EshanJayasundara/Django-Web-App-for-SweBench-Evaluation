from django.urls import path
from .views import SampleAPIView, SweAPIView, FileUploadView

urlpatterns = [
    path('test/', SampleAPIView.as_view()),
    path('swe_eval/', SweAPIView.as_view()),
    path('file_upload/', FileUploadView.as_view()),
]