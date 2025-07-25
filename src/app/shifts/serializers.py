from rest_framework import serializers

from shifts.helpers import build_time_punch_graph_series
from shifts.models import TimePunchFile, TimePunch


class TimePunchFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = TimePunchFile
        fields = [
            'id', 'created_at', 'updated_at', 'name', 'code',
            'fingerprint', 'punch_count', 'status'
        ]


class TimePunchSerializer(serializers.ModelSerializer):
    time_punch_file = serializers.SerializerMethodField()

    def get_time_punch_file(self, obj):
        return obj.time_punch_file.name

    class Meta:
        model = TimePunch
        fields = ['id', 'punch_date', 'punch_hour', 'employee_number', 'time_punch_file']
        read_only_fields = [*fields]


class TimePunchGraphSeriesSerializer(serializers.ModelSerializer):
    graph_series = serializers.SerializerMethodField()

    def get_graph_series(self, obj):
        punch_date = self.context.get('punch_date')

        if punch_date is not None:
            return build_time_punch_graph_series(punch_date)

        return {}

    class Meta:
        model = TimePunch
        fields = ['graph_series']
