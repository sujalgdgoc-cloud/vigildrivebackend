from rest_framework import generics

from .models import (
    DriverInfoModel,
    DriverSafetyScan,
)

from .serializers import (
    DriverInfoSerializers,
    DriverSafetyScanSerializer,
)


# ============================================================
# DRIVER INFORMATION
# ============================================================

class DriverInfoView(generics.ListCreateAPIView):

    queryset = DriverInfoModel.objects.all()

    serializer_class = DriverInfoSerializers


# ============================================================
# DRIVER SAFETY SCANS
# ============================================================

class DriverSafetyScanListCreateView(
    generics.ListCreateAPIView
):

    queryset = DriverSafetyScan.objects.all()

    serializer_class = DriverSafetyScanSerializer


# ============================================================
# SINGLE SAFETY SCAN
# ============================================================

class DriverSafetyScanDetailView(
    generics.RetrieveDestroyAPIView
):

    queryset = DriverSafetyScan.objects.all()

    serializer_class = DriverSafetyScanSerializer