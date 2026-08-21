from django.urls import path
from .views import DriverInfoView, DriverInfoDetailView, DriverSafetyScanDetailView, DriverSafetyScanListCreateView
urlpatterns = [
    path("driverinfo/", DriverInfoView.as_view()),
    path("driverinfo/<int:pk>/", DriverInfoDetailView.as_view()),
    path("driverdata/<int:pk>/", DriverSafetyScanDetailView.as_view()),
    path("driverdata/", DriverSafetyScanListCreateView.as_view())
]