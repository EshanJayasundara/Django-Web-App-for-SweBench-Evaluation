from django.urls import path
from .views import SampleAPIView, SweAPIView

urlpatterns = [
    path('test/', SampleAPIView.as_view(), name='test'),
    path('swe_eval/', SweAPIView.as_view()),
]