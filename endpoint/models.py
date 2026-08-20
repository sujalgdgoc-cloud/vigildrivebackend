
from django.db import models
from django.conf import settings

class DriverInfoModel(models.Model):
    class Status(models.TextChoices):
        PLANNED = 'PLANNED', 'Planned'
        IN_PROGRESS = 'IN_PROGRESS', 'In Progress'
        COMPLETED = 'COMPLETED', 'Completed'

    driver = models.CharField(max_length=30)
    
    truck_id = models.CharField(max_length=20)
    truck_no = models.CharField(max_length=20)
    

    start_point = models.CharField(max_length=100)
    end_point = models.CharField(max_length=100)
    
    
    lat = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    lon = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    
   
    status = models.CharField(max_length=15, choices=Status.choices, default=Status.PLANNED)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Driver Info"
        verbose_name_plural = "Driver Info Logs"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.truck_no} - {self.start_point} to {self.end_point}"

from django.db import models

class DriverSafetyScan(models.Model):
    status = models.CharField(max_length=50)
    total_frames_processed = models.PositiveIntegerField()
    overall_risk_score = models.IntegerField()
    risk_level = models.CharField(max_length=20)
    environment_warning = models.CharField(max_length=255)
    spoof_detected = models.BooleanField(default=False)
    spoof_reasons = models.JSONField(default=list)
    final_perclos = models.FloatField()
    max_blink_duration_ms = models.IntegerField()
    scan_timestamp = models.DateTimeField()
    
    # Motion Analysis Fields
    sudden_braking_detected = models.BooleanField(default=False)
    sudden_braking_events = models.PositiveIntegerField(default=0)
    swerving_detected = models.BooleanField(default=False)
    swerving_events = models.PositiveIntegerField(default=0)
    accelerometer_samples = models.PositiveIntegerField(default=0)
    gyroscope_samples = models.PositiveIntegerField(default=0)
    max_acceleration_magnitude = models.FloatField()
    average_acceleration_magnitude = models.FloatField()
    max_gyroscope_magnitude = models.FloatField()
    accelerometer_data = models.JSONField(default=list)
    gyroscope_data = models.JSONField(default=list)

    def __str__(self):
        return f"Scan {self.id} - Risk: {self.risk_level} ({self.overall_risk_score})"