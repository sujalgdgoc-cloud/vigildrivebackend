from django.db import models


# ============================================================
# DRIVER INFO
# ============================================================

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

    lat = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        null=True,
        blank=True,
    )

    lon = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        null=True,
        blank=True,
    )

    status = models.CharField(
        max_length=15,
        choices=Status.choices,
        default=Status.PLANNED,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        verbose_name = "Driver Info"
        verbose_name_plural = "Driver Info Logs"
        ordering = ["-created_at"]

    def __str__(self):
        return (
            f"{self.truck_no} - "
            f"{self.start_point} to {self.end_point}"
        )


# ============================================================
# DRIVER SAFETY SCAN
# ============================================================

class DriverSafetyScan(models.Model):

    # ========================================================
    # TRUCK
    # ========================================================

    truck_id = models.CharField(
        max_length=20,
    )

    # ========================================================
    # SAFETY ANALYSIS
    # ========================================================

    status = models.CharField(
        max_length=50,
        default="success",
    )

    total_frames_processed = models.PositiveIntegerField(
        default=0,
    )

    overall_risk_score = models.IntegerField(
        default=0,
    )

    risk_level = models.CharField(
        max_length=20,
        default="UNKNOWN",
    )

    environment_warning = models.CharField(
        max_length=255,
        default="No environment warning",
        blank=True,
    )

    spoof_detected = models.BooleanField(
        default=False,
    )

    spoof_reasons = models.JSONField(
        default=list,
        blank=True,
    )

    final_perclos = models.FloatField(
        default=0.0,
    )

    max_blink_duration_ms = models.IntegerField(
        default=0,
    )

    scan_timestamp = models.DateTimeField()

    # ========================================================
    # MOTION ANALYSIS
    # ========================================================

    sudden_braking_detected = models.BooleanField(
        default=False,
    )

    sudden_braking_events = models.PositiveIntegerField(
        default=0,
    )

    swerving_detected = models.BooleanField(
        default=False,
    )

    swerving_events = models.PositiveIntegerField(
        default=0,
    )

    accelerometer_samples = models.PositiveIntegerField(
        default=0,
    )

    gyroscope_samples = models.PositiveIntegerField(
        default=0,
    )

    max_acceleration_magnitude = models.FloatField(
        default=0.0,
    )

    average_acceleration_magnitude = models.FloatField(
        default=0.0,
    )

    max_gyroscope_magnitude = models.FloatField(
        default=0.0,
    )

    accelerometer_data = models.JSONField(
        default=list,
        blank=True,
    )

    gyroscope_data = models.JSONField(
        default=list,
        blank=True,
    )

    class Meta:
        verbose_name = "Safety Scan"
        verbose_name_plural = "Safety Scans"
        ordering = ["-scan_timestamp"]

    def __str__(self):
        return (
            f"Scan {self.id} - "
            f"Truck: {self.truck_id} - "
            f"Risk: {self.risk_level} "
            f"({self.overall_risk_score})"
        )