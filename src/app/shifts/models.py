from django.db import models

from common.models import TimeStampedAbstractModel


class TimePunchFile(TimeStampedAbstractModel):
    name = models.CharField(max_length=255)
    punch_count = models.IntegerField()
    fingerprint = models.CharField(max_length=255, unique=True)


class TimePunch(TimeStampedAbstractModel):
    time_punch_file = models.ForeignKey(
        TimePunchFile, on_delete=models.CASCADE, related_name='time_punches'
    )

    punch_date = models.DateField()
    punch_hour = models.TimeField()
    employee_number = models.IntegerField()
