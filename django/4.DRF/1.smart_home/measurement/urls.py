from django.urls import path
from .views import SensorListCreateAPIView, SensorRetrieveUpdateAPIView, MeasurementCreateAPIView

urlpatterns = [
    # TODO: зарегистрируйте необходимые маршруты
    path('sensors/', SensorListCreateAPIView.as_view()),
    path('sensors/<pk>/', SensorRetrieveUpdateAPIView.as_view()),
    path('measurements/', MeasurementCreateAPIView.as_view()),
]
