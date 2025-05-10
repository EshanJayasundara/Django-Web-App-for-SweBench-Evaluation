from django.urls import path
from .views import SampleAPIView, GenerateApiKeyView

urlpatterns = [
    path('swe_eval/', SampleAPIView.as_view()),       # GET all, POST create
]