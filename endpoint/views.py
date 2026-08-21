from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status as http_status

from .models import (
    DriverInfoModel,
    DriverSafetyScan,
)

from .serializers import (
    DriverInfoSerializers,
    DriverSafetyScanSerializer,
)


# ============================================================
# DRIVER INFO
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

    def create(self, request, *args, **kwargs):

        print("========================================")
        print("SAFETY SCAN POST RECEIVED")
        print("========================================")

        print("REQUEST DATA:")
        print(request.data)

        serializer = self.get_serializer(
            data=request.data
        )

        if not serializer.is_valid():

            print("========================================")
            print("SERIALIZER ERRORS")
            print(serializer.errors)
            print("========================================")

            return Response(
                {
                    "success": False,
                    "errors": serializer.errors,
                },
                status=http_status.HTTP_400_BAD_REQUEST,
            )

        try:

            scan = serializer.save()

            print("========================================")
            print("SAFETY SCAN SAVED")
            print("ID:", scan.id)
            print("TRUCK ID:", scan.truck_id)
            print("RISK LEVEL:", scan.risk_level)
            print("RISK SCORE:", scan.overall_risk_score)
            print("========================================")

            return Response(
                self.get_serializer(scan).data,
                status=http_status.HTTP_201_CREATED,
            )

        except Exception as e:

            print("========================================")
            print("DATABASE SAVE ERROR")
            print(repr(e))
            print("========================================")

            return Response(
                {
                    "success": False,
                    "error": str(e),
                },
                status=http_status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


# ============================================================
# SINGLE SAFETY SCAN
# ============================================================

class DriverSafetyScanDetailView(
    generics.RetrieveDestroyAPIView
):

    queryset = DriverSafetyScan.objects.all()

    serializer_class = DriverSafetyScanSerializer