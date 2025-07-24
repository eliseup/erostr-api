from rest_framework import serializers

from shifts.models import TimePunchFile, TimePunch


class TimePunchFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = TimePunchFile
        fields = '__all__'


class TimePunchSerializer(serializers.ModelSerializer):
    class Meta:
        model = TimePunch
        fields = '__all__'
        read_only_fields = '__all__'
