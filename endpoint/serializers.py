from rest_framework import serializers

from .models import (
    DriverInfoModel,
    DriverSafetyScan,
)


# ============================================================
# DRIVER INFO SERIALIZER
# ============================================================

class DriverInfoSerializers(serializers.ModelSerializer):

    class Meta:
        model = DriverInfoModel
        fields = "__all__"


# ============================================================
# DRIVER SAFETY SCAN SERIALIZER
# ============================================================

class DriverSafetyScanSerializer(serializers.ModelSerializer):

    class Meta:
        model = DriverSafetyScan

        fields = [
            "id",

            # FastAPI analysis
            "status",
            "total_frames_processed",
            "overall_risk_score",
            "risk_level",
            "environment_warning",
            "spoof_detected",
            "spoof_reasons",
            "final_perclos",
            "max_blink_duration_ms",

            # Timestamp
            "scan_timestamp",

            # Motion analysis
            "sudden_braking_detected",
            "sudden_braking_events",
            "swerving_detected",
            "swerving_events",
            "accelerometer_samples",
            "gyroscope_samples",
            "max_acceleration_magnitude",
            "average_acceleration_magnitude",
            "max_gyroscope_magnitude",

            # Raw sensor data
            "accelerometer_data",
            "gyroscope_data",
        ]

        read_only_fields = [
            "id",
        ]