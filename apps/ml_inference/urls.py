from django.urls import path
from .views import InferenceAPIView, HistoryAPIView, DetailAPIView

app_name = 'ml_inference'

urlpatterns = [
    path('inference/', InferenceAPIView.as_view(), name='inference'),
    path('history/', HistoryAPIView.as_view(), name='history'),
    path('inference/<int:request_id>/', DetailAPIView.as_view(), name='detail'),
]
