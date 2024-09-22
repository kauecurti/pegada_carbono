from django.urls import path
from .views import CalcularPegadaAPIView

urlpatterns = [
    path('calcular-pegada/', CalcularPegadaAPIView.as_view(), name='calcular_pegada'),
]
