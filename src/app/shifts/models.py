from django.db import models

from common.models import TimeStampedAbstractModel


class TimePunchFile(TimeStampedAbstractModel):
    STATUS_CHOICES = (
        ('success', 'Sucesso'),
        ('error', 'Erro'),
        ('in_progress', 'Em andamento'),
    )

    name = models.CharField(max_length=255, blank=True)
    code = models.CharField(max_length=255, unique=True, blank=True)
    punch_count = models.IntegerField(null=True, blank=True)
    fingerprint = models.CharField(max_length=255, unique=True, null=True, blank=True)
    status = models.CharField(max_length=45, choices=STATUS_CHOICES, default='in_progress')


class TimePunch(TimeStampedAbstractModel):
    time_punch_file = models.ForeignKey(
        TimePunchFile, on_delete=models.CASCADE, related_name='time_punches'
    )

    punch_date = models.DateField()
    punch_hour = models.TimeField()
    employee_number = models.IntegerField()
