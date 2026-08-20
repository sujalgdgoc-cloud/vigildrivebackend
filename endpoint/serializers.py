from rest_framework import serializers

from .models import DriverInfoModel, DriverSafetyScan


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
    sudden_braking_detected = serializers.BooleanField(default=False)
    sudden_braking_events = serializers.IntegerField(default=0)

    swerving_detected = serializers.BooleanField(default=False)
    swerving_events = serializers.IntegerField(default=0)

    accelerometer_samples = serializers.IntegerField(default=0)
    gyroscope_samples = serializers.IntegerField(default=0)

    max_acceleration_magnitude = serializers.FloatField(default=0.0)
    average_acceleration_magnitude = serializers.FloatField(default=0.0)
    max_gyroscope_magnitude = serializers.FloatField(default=0.0)

    accelerometer_data = serializers.ListField(
        child=serializers.DictField(),
        required=False,
        default=list
    )

    gyroscope_data = serializers.ListField(
        child=serializers.DictField(),
        required=False,
        default=list
    )


# ============================================================
# DRIVER SAFETY SCAN SERIALIZER
# ============================================================

class DriverSafetyScanSerializer(serializers.ModelSerializer):

    # FastAPI can return null.
    # Django model stores a CharField, so convert null/blank
    # into a safe string before saving.
    environment_warning = serializers.CharField(
        max_length=255,
        required=False,
        allow_blank=True,
        allow_null=True,
        default="No environment warning"
    )

    # Flutter sends motion_analysis as a nested JSON object.
    motion_analysis = MotionAnalysisSerializer(
        required=False,
        default=dict
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

        read_only_fields = ["id"]

    def validate_environment_warning(self, value):
        """
        FastAPI may return null.

        Store a normal string in Django instead of allowing
        None to reach the CharField.
        """

        if value is None or str(value).strip() == "":
            return "No environment warning"

        return value

    def create(self, validated_data):
        """
        Convert Flutter's nested motion_analysis object into
        the individual DriverSafetyScan model fields.
        """

        motion_analysis = validated_data.pop(
            "motion_analysis",
            {}
        )

        # ----------------------------------------------------
        # Environment warning
        # ----------------------------------------------------

        environment_warning = validated_data.get(
            "environment_warning"
        )

        if environment_warning is None or str(
            environment_warning
        ).strip() == "":
            validated_data["environment_warning"] = (
                "No environment warning"
            )

        # ----------------------------------------------------
        # Motion analysis
        # ----------------------------------------------------

        validated_data["sudden_braking_detected"] = (
            motion_analysis.get(
                "sudden_braking_detected",
                False
            )
        )

        validated_data["sudden_braking_events"] = (
            motion_analysis.get(
                "sudden_braking_events",
                0
            )
        )

        validated_data["swerving_detected"] = (
            motion_analysis.get(
                "swerving_detected",
                False
            )
        )

        validated_data["swerving_events"] = (
            motion_analysis.get(
                "swerving_events",
                0
            )
        )

        validated_data["accelerometer_samples"] = (
            motion_analysis.get(
                "accelerometer_samples",
                0
            )
        )

        validated_data["gyroscope_samples"] = (
            motion_analysis.get(
                "gyroscope_samples",
                0
            )
        )

        validated_data["max_acceleration_magnitude"] = (
            motion_analysis.get(
                "max_acceleration_magnitude",
                0.0
            )
        )

        validated_data["average_acceleration_magnitude"] = (
            motion_analysis.get(
                "average_acceleration_magnitude",
                0.0
            )
        )

        validated_data["max_gyroscope_magnitude"] = (
            motion_analysis.get(
                "max_gyroscope_magnitude",
                0.0
            )
        )

        validated_data["accelerometer_data"] = (
            motion_analysis.get(
                "accelerometer_data",
                []
            )
        )

        validated_data["gyroscope_data"] = (
            motion_analysis.get(
                "gyroscope_data",
                []
            )
        )

        # ----------------------------------------------------
        # Finally create the database record
        # ----------------------------------------------------

        return DriverSafetyScan.objects.create(
            **validated_data
        )