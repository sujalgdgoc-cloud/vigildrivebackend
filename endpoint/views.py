from django.shortcuts import render
from rest_framework import generics
from rest_framework.response import Response
from .models import DriverInfoModel, DriverSafetyScan
from .serializers import DriverInfoSerializers, DriverSafetyScanSerializer
class DriverInfoView(generics.ListCreateAPIView):
    queryset = DriverInfoModel.objects.all()
    serializer_class = DriverInfoSerializers

class DriverSafetyScanListCreateView(generics.ListCreateAPIView):
    queryset = DriverSafetyScan.objects.all()
    serializer_class = DriverSafetyScanSerializer

class DriverSafetyScanDetailView(generics.RetrieveDestroyAPIView):
    queryset = DriverSafetyScan.objects.all()
    serializer_class = DriverSafetyScanSerializer