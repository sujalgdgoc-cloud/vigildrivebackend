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
# MOTION ANALYSIS SERIALIZER
# ============================================================

class MotionAnalysisSerializer(serializers.Serializer):

    sudden_braking_detected = serializers.BooleanField(
        required=False,
        default=False,
    )

    sudden_braking_events = serializers.IntegerField(
        required=False,
        default=0,
    )

    swerving_detected = serializers.BooleanField(
        required=False,
        default=False,
    )

    swerving_events = serializers.IntegerField(
        required=False,
        default=0,
    )

    accelerometer_samples = serializers.IntegerField(
        required=False,
        default=0,
    )

    gyroscope_samples = serializers.IntegerField(
        required=False,
        default=0,
    )

    max_acceleration_magnitude = serializers.FloatField(
        required=False,
        default=0.0,
    )

    average_acceleration_magnitude = serializers.FloatField(
        required=False,
        default=0.0,
    )

    max_gyroscope_magnitude = serializers.FloatField(
        required=False,
        default=0.0,
    )

    accelerometer_data = serializers.ListField(
        child=serializers.DictField(),
        required=False,
        default=list,
    )

    gyroscope_data = serializers.ListField(
        child=serializers.DictField(),
        required=False,
        default=list,
    )


# ============================================================
# DRIVER SAFETY SCAN SERIALIZER
# ============================================================

class DriverSafetyScanSerializer(
    serializers.ModelSerializer
):

    motion_analysis = MotionAnalysisSerializer(
        required=False,
        default=dict,
    )

    environment_warning = serializers.CharField(
        required=False,
        allow_blank=True,
        allow_null=True,
        default="No environment warning",
    )

    class Meta:

        model = DriverSafetyScan

        fields = [
            "id",

            "status",
            "total_frames_processed",
            "overall_risk_score",
            "risk_level",
            "environment_warning",

            "spoof_detected",
            "spoof_reasons",

            "final_perclos",
            "max_blink_duration_ms",

            "motion_analysis",

            "scan_timestamp",

            "sudden_braking_detected",
            "sudden_braking_events",

            "swerving_detected",
            "swerving_events",

            "accelerometer_samples",
            "gyroscope_samples",

            "max_acceleration_magnitude",
            "average_acceleration_magnitude",
            "max_gyroscope_magnitude",

            "accelerometer_data",
            "gyroscope_data",
        ]

        read_only_fields = [
            "id",
        ]

    def validate_environment_warning(self, value):

        if value is None:
            return "No environment warning"

        value = str(value).strip()

        if not value:
            return "No environment warning"

        return value

    def validate(self, attrs):

        # ----------------------------------------------------
        # Safe defaults for FastAPI null values
        # ----------------------------------------------------

        attrs["status"] = (
            attrs.get("status")
            or "success"
        )

        attrs["total_frames_processed"] = (
            attrs.get("total_frames_processed")
            or 0
        )

        attrs["overall_risk_score"] = (
            attrs.get("overall_risk_score")
            or 0
        )

        attrs["risk_level"] = (
            attrs.get("risk_level")
            or "UNKNOWN"
        )

        attrs["spoof_detected"] = (
            attrs.get("spoof_detected")
            if attrs.get("spoof_detected") is not None
            else False
        )

        attrs["spoof_reasons"] = (
            attrs.get("spoof_reasons")
            or []
        )

        attrs["final_perclos"] = (
            attrs.get("final_perclos")
            or 0.0
        )

        attrs["max_blink_duration_ms"] = (
            attrs.get("max_blink_duration_ms")
            or 0
        )

        attrs["scan_timestamp"] = (
            attrs.get("scan_timestamp")
        )

        # ----------------------------------------------------
        # Motion analysis
        # ----------------------------------------------------

        motion = attrs.get(
            "motion_analysis",
            {}
        )

        attrs["sudden_braking_detected"] = (
            motion.get(
                "sudden_braking_detected",
                False,
            )
        )

        attrs["sudden_braking_events"] = (
            motion.get(
                "sudden_braking_events",
                0,
            )
        )

        attrs["swerving_detected"] = (
            motion.get(
                "swerving_detected",
                False,
            )
        )

        attrs["swerving_events"] = (
            motion.get(
                "swerving_events",
                0,
            )
        )

        attrs["accelerometer_samples"] = (
            motion.get(
                "accelerometer_samples",
                0,
            )
        )

        attrs["gyroscope_samples"] = (
            motion.get(
                "gyroscope_samples",
                0,
            )
        )

        attrs["max_acceleration_magnitude"] = (
            motion.get(
                "max_acceleration_magnitude",
                0.0,
            )
        )

        attrs["average_acceleration_magnitude"] = (
            motion.get(
                "average_acceleration_magnitude",
                0.0,
            )
        )

        attrs["max_gyroscope_magnitude"] = (
            motion.get(
                "max_gyroscope_magnitude",
                0.0,
            )
        )

        attrs["accelerometer_data"] = (
            motion.get(
                "accelerometer_data",
                [],
            )
        )

        attrs["gyroscope_data"] = (
            motion.get(
                "gyroscope_data",
                [],
            )
        )

        # Remove nested object because the model
        # does not have a motion_analysis column.

        attrs.pop(
            "motion_analysis",
            None,
        )

        return attrs

    def create(self, validated_data):

        return DriverSafetyScan.objects.create(
            **validated_data
        )