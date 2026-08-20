from rest_framework import serializers
from .models import DriverInfoModel

class DriverInfoSerializers(serializers.ModelSerializer):
    class Meta:
        model = DriverInfoModel
        fields = "__all__"

from rest_framework import serializers

class MotionAnalysisSerializer(serializers.Serializer):
    sudden_braking_detected = serializers.BooleanField()
    sudden_braking_events = serializers.IntegerField()
    swerving_detected = serializers.BooleanField()
    swerving_events = serializers.IntegerField()
    accelerometer_samples = serializers.IntegerField()
    gyroscope_samples = serializers.IntegerField()
    max_acceleration_magnitude = serializers.FloatField()
    average_acceleration_magnitude = serializers.FloatField()
    max_gyroscope_magnitude = serializers.FloatField()
    accelerometer_data = serializers.ListField(child=serializers.DictField(), default=list)
    gyroscope_data = serializers.ListField(child=serializers.DictField(), default=list)

class DriverSafetyScanSerializer(serializers.Serializer):
    status = serializers.CharField(max_length=50)
    total_frames_processed = serializers.IntegerField()
    overall_risk_score = serializers.IntegerField()
    risk_level = serializers.CharField(max_length=20)
    environment_warning = serializers.CharField(max_length=255)
    spoof_detected = serializers.BooleanField()
    spoof_reasons = serializers.ListField(child=serializers.CharField(), default=list)
    final_perclos = serializers.FloatField()
    max_blink_duration_ms = serializers.IntegerField()
    motion_analysis = MotionAnalysisSerializer()
    scan_timestamp = serializers.DateTimeField()