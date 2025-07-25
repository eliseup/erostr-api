from rest_framework import serializers

from shifts.models import TimePunchFile, TimePunch


class TimePunchFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = TimePunchFile
        fields = ['id', 'name', 'code', 'fingerprint', 'punch_count', 'status']


class TimePunchSerializer(serializers.ModelSerializer):
    class Meta:
        model = TimePunch
        fields = ['id', 'punch_date', 'punch_hour', 'employee_number', 'time_punch_file']
        read_only_fields = [*fields]
