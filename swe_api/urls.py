from django.urls import path
from .views import SampleAPIView, GenerateApiKeyView

urlpatterns = [
    path('swe_eval/', SampleAPIView.as_view()),       # GET all, POST create
    # path('item/<str:id>/', SampleAPIView.as_view()),  # GET one, PUT update, DELETE
    path('generate-api-key/', GenerateApiKeyView.as_view(), name='generate_api_key'),
]