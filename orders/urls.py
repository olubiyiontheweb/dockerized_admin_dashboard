from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import OrderGenericAPIView, ExportAPIView, ChartAPIView

urlpatterns = [
    path('orders/', OrderGenericAPIView.as_view()),
    path('orders/<str:pk>', OrderGenericAPIView.as_view()),
    path('export', ExportAPIView.as_view()),
    path('chart', ChartAPIView.as_view())
]